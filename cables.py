"""
cables.py

Moduł obsługujący logikę kabli w grze.

Założenia:
- Kablami są obiekty typu "long_rect" trzymane w ObjectManager.objects.
- Ten moduł NIE tworzy ani nie rysuje obiektów gry – tylko:
  * wykrywa, które obiekty są kablami,
  * buduje z nich graf połączeń,
  * potrafi policzyć propagację "prądu" od źródeł do pozostałych kabli / odbiorników.

Użycie – przykład (w głównym pliku gry):

    from cables import CableManager

    cable_mgr = CableManager(max_conn_distance=5)

    # w pętli gry po zaktualizowaniu ObjectManager.objects:
    cable_mgr.sync_from_objects(objects.objects)

    # Źródła prądu – np. obiekty elektrowni:
    power_sources = [obj for obj in objects.objects if obj.kind == "power_plant"]

    # Odbiorniki – np. domki:
    consumers = [obj for obj in objects.objects if obj.kind == "house"]

    cable_mgr.update_power_state(power_sources, consumers)

    # teraz:
    # - każdy CableInfo w cable_mgr.cables ma pole .powered
    # - każdy odbiornik z listy consumers pojawia się w cable_mgr.powered_consumers
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Any, Dict, Set, Tuple, Iterable, Optional
import math


@dataclass
class CableInfo:
    """
    Reprezentacja pojedynczego odcinka kabla – w Twojej grze odpowiada
    jednemu obiektowi typu "long_rect".

    `game_object` – oryginalny obiekt z ObjectManager.objects (np. rect, shape, itd.)
    """
    game_object: Any
    center: Tuple[float, float]
    powered: bool = False

    @property
    def x(self) -> float:
        return self.center[0]

    @property
    def y(self) -> float:
        return self.center[1]


class CableManager:
    """
    Główny menedżer kabli:
      - zbiera z ObjectManager.objects wszystkie kable (shape == 'long_rect'),
      - buduje graf połączeń między nimi na podstawie odległości,
      - propaguje 'prąd' od źródeł do kabli i dalej do odbiorników.
    """

    def __init__(self, max_conn_distance: float = 70.0) -> None:
        """
        :param max_conn_distance: maksymalna odległość między środkami dwóch kabli,
                                  przy której traktujemy je jako połączone.
                                  Dostosuj do rozmiaru swoich long_rect.
        """
        self.max_conn_distance = max_conn_distance
        self.cables: List[CableInfo] = []
        # adjacency: indeks kabla -> zbiór indeksów kabli połączonych
        self.graph: Dict[int, Set[int]] = {}
        # odbiorniki, które aktualnie mają prąd
        self.powered_consumers: Set[Any] = set()

    # ------------------------------------------------------------------
    # Synchronizacja z obiektami gry
    # ------------------------------------------------------------------

    def sync_from_objects(self, objects: Iterable[Any]) -> None:
        """
        Wczytuje z listy obiektów tylko te, które są kablami (shape == 'long_rect'),
        i tworzy z nich wewnętrzną listę CableInfo.

        Zakładam, że każdy obiekt ma:
          - atrybut 'shape' == "long_rect"
          - atrybut 'rect' typu pygame.Rect lub podobny z .center

        Jeśli Twoje obiekty nazywają się inaczej, zaktualizuj to miejsce.
        """
        self.cables.clear()

        for obj in objects:
            shape = getattr(obj, "shape", None)
            if shape != "long_rect":
                continue

            rect = getattr(obj, "rect", None)
            if rect is None or not hasattr(rect, "center"):
                # Jeśli Twoje obiekty nie mają rect.center,
                # dostosuj sposób wyznaczania środka:
                # center = (obj.x, obj.y) albo podobnie.
                continue

            center = rect.center
            self.cables.append(CableInfo(game_object=obj, center=center))

        self._build_graph()

    # ------------------------------------------------------------------
    # Budowanie grafu połączeń
    # ------------------------------------------------------------------

    def _build_graph(self) -> None:
        """
        Tworzy graf połączeń pomiędzy kablami na podstawie odległości
        między ich środkami.

        Dwa kable są połączone, jeśli odległość ich środków
        jest mniejsza lub równa max_conn_distance.
        """
        self.graph = {i: set() for i in range(len(self.cables))}

        for i, cable_a in enumerate(self.cables):
            for j in range(i + 1, len(self.cables)):
                cable_b = self.cables[j]
                if self._are_neighbors(cable_a, cable_b):
                    self.graph[i].add(j)
                    self.graph[j].add(i)

    def _are_neighbors(self, a: CableInfo, b: CableInfo) -> bool:
        """
        Sprawdza, czy dwa kable są wystarczająco blisko, aby traktować je
        jako połączone.

        Jeśli wolisz dokładniejsze sprawdzanie (np. dotykanie krawędzi rect),
        możesz przerobić tę funkcję.
        """
        dx = a.x - b.x
        dy = a.y - b.y
        dist_sq = dx * dx + dy * dy
        return dist_sq <= self.max_conn_distance * self.max_conn_distance

    # ------------------------------------------------------------------
    # Logika zasilania
    # ------------------------------------------------------------------

    def update_power_state(
        self,
        power_sources: Iterable[Any],
        consumers: Iterable[Any],
    ) -> None:
        """
        Liczy, które kable i odbiorniki są zasilane.

        :param power_sources: iterable obiektów gry (np. elektrownie), które są źródłami prądu.
                              Zakładam, że każdy taki obiekt ma rect.center albo inne
                              pole położenia – dostosuj w razie potrzeby.
        :param consumers: iterable obiektów gry (np. domki), które mogą być odbiornikami.
        """

        # 1. Reset stanu zasilania
        for cable in self.cables:
            cable.powered = False
        self.powered_consumers.clear()

        # 2. Znajdź, które kable są najbliżej źródeł (start BFS)
        start_indices: Set[int] = set()

        for src in power_sources:
            src_center = self._get_object_center(src)
            if src_center is None:
                continue

            idx = self._find_nearest_cable_index(src_center)
            if idx is not None:
                start_indices.add(idx)

        # 3. Propagacja "prądu" po grafie (BFS)
        powered_indices = self._bfs_from(start_indices)

        # 4. Ustaw flagi .powered na kablach
        for idx in powered_indices:
            self.cables[idx].powered = True

        # 5. Sprawdź, które odbiorniki są podłączone do zasilanych kabli
        for cons in consumers:
            cons_center = self._get_object_center(cons)
            if cons_center is None:
                continue

            nearest_idx = self._find_nearest_cable_index(cons_center)
            if nearest_idx is not None and nearest_idx in powered_indices:
                self.powered_consumers.add(cons)

    def _get_object_center(self, obj: Any) -> Optional[Tuple[float, float]]:
        """
        Wyciąga środek obiektu gry.

        Zakładam, że:
          - obiekt ma rect.center
        Jeśli jest inaczej, zmień tę funkcję na coś w stylu:
          return (obj.x, obj.y)
        """
        rect = getattr(obj, "rect", None)
        if rect is None or not hasattr(rect, "center"):
            return None
        return rect.center

    def _find_nearest_cable_index(
        self,
        point: Tuple[float, float],
    ) -> Optional[int]:
        """
        Znajduje indeks kabla, którego środek jest najbliżej podanego punktu.

        Jeśli nie ma żadnych kabli, zwraca None.
        """
        if not self.cables:
            return None

        px, py = point
        best_idx = None
        best_dist_sq = float("inf")

        for i, cable in enumerate(self.cables):
            dx = cable.x - px
            dy = cable.y - py
            dist_sq = dx * dx + dy * dy
            if dist_sq < best_dist_sq:
                best_dist_sq = dist_sq
                best_idx = i

        return best_idx

    def _bfs_from(self, start_indices: Iterable[int]) -> Set[int]:
        """
        BFS po grafie kabli, zaczynając od indeksów w `start_indices`.

        Zwraca zbiór indeksów kabli, do których "dotarł prąd".
        """
        visited: Set[int] = set()
        queue: List[int] = []

        for idx in start_indices:
            if 0 <= idx < len(self.cables):
                visited.add(idx)
                queue.append(idx)

        while queue:
            current = queue.pop(0)
            for neighbor in self.graph.get(current, ()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return visited

    # ------------------------------------------------------------------
    # Funkcje pomocnicze / debug
    # ------------------------------------------------------------------

    def get_powered_cable_objects(self) -> List[Any]:
        """
        Zwraca listę oryginalnych obiektów gry (long_rect),
        które są aktualnie zasilane.
        """
        return [c.game_object for c in self.cables if c.powered]

    def get_all_cable_objects(self) -> List[Any]:
        """
        Zwraca listę wszystkich obiektów gry reprezentujących kable.
        """
        return [c.game_object for c in self.cables]
