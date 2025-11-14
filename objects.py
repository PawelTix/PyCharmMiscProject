import pygame
from collections import deque


class GameObject(pygame.sprite.Sprite):
    """
    Prosty sprite obiektu w grze.
    kind: "triangle", "tall_rect", "long_rect", "wall", ...
    rect: pygame.Rect – pozycja i rozmiar obiektu
    """

    def __init__(self, kind: str, rect: pygame.Rect):
        super().__init__()
        self.kind = kind
        self.rect = rect.copy()

        # Na razie generujemy prosty surface – logika rysowania i tak
        # jest w ObjectManager.draw (trójkąty itp.).
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)


class ObjectManager:
    def __init__(self):
        # przechowujemy sprite’y w grupie
        self.group = pygame.sprite.Group()

    @property
    def objects(self):
        """Zachowujemy kompatybilny interfejs – zwraca listę sprite’ów."""
        return list(self.group.sprites())

    # =================== DODAWANIE / USUWANIE ===================

    def add_object(self, shape: str, rect: pygame.Rect):
        obj = GameObject(shape, rect)
        self.group.add(obj)
        return obj

    def add_wall(self, rect: pygame.Rect):
        return self.add_object("wall", rect)

    def remove_at_point(self, pos):
        x, y = pos
        # od końca – żeby bezpiecznie usuwać
        for obj in reversed(self.objects):
            if obj.kind == "wall":
                continue  # NIE pozwalamy usuwać ścian
            if obj.rect.collidepoint(x, y):
                self.group.remove(obj)
                return True
        return False

    # =================== LOGIKA POŁĄCZEŃ ===================

    @staticmethod
    def _rect_connected(r1: pygame.Rect, r2: pygame.Rect) -> bool:
        """Czy dwa recty się łączą? (dotyk lub nachodzenie)"""
        if r1.colliderect(r2):
            return True

        # dotykanie boków w poziomie
        if r1.right == r2.left or r2.right == r1.left:
            if not (r1.bottom < r2.top or r1.top > r2.bottom):
                return True

        # dotykanie boków w pionie
        if r1.bottom == r2.top or r2.bottom == r1.top:
            if not (r1.right < r2.left or r1.left > r2.right):
                return True

        return False

    def compute_powered(self):
        """Zwraca indeksy obiektów, które mają połączenie z elektrownią (triangle)."""
        objs = self.objects
        n = len(objs)
        if n == 0:
            return set()

        # Znajdź elektrownie
        power_plants = [i for i, obj in enumerate(objs) if obj.kind == "triangle"]
        if not power_plants:
            return set()

        # Budujemy graf połączeń
        adj = [[] for _ in range(n)]
        for i in range(n):
            si = objs[i].kind
            ri = objs[i].rect
            if si not in ("triangle", "tall_rect", "long_rect"):
                continue

            for j in range(i + 1, n):
                sj = objs[j].kind
                rj = objs[j].rect
                if sj not in ("triangle", "tall_rect", "long_rect"):
                    continue

                if self._rect_connected(ri, rj):
                    adj[i].append(j)
                    adj[j].append(i)

        # BFS od elektrowni
        visited = set(power_plants)
        q = deque(power_plants)

        while q:
            v = q.popleft()
            for nei in adj[v]:
                if nei not in visited:
                    visited.add(nei)
                    q.append(nei)

        return visited

    # =================== RYSOWANIE ===================

    def draw(self, screen, powered=None):
        if powered is None:
            powered = set()

        objs = self.objects

        # --- WNĘTRZNE ŚCIANY ---
        for obj in objs:
            if obj.kind == "wall":
                pygame.draw.rect(screen, (80, 80, 80), obj.rect)
        # --- RESZTA OBIEKTÓW ---
        for idx, obj in enumerate(objs):
            shape = obj.kind
            rect = obj.rect

            if shape == "wall":
                continue

            # kolory bazowe
            if shape == "triangle":
                base = (200, 180, 40)
            elif shape == "tall_rect":
                base = (150, 80, 80)
            elif shape == "long_rect":
                base = (120, 120, 120)
            else:
                base = (40, 80, 200)

            # prąd?
            if idx in powered:
                if shape == "triangle":
                    color = (255, 255, 0)
                elif shape == "long_rect":
                    color = (0, 180, 250)
                elif shape == "tall_rect":
                    color = (0, 255, 0)
                else:
                    color = base
            else:
                color = base

            # rysowanie
            if shape in ("square", "tall_rect", "long_rect"):
                pygame.draw.rect(screen, color, rect)
            elif shape == "triangle":
                x, y, w, h = rect
                pts = [
                    (x + w // 2, y),
                    (x, y + h),
                    (x + w, y + h)
                ]
                pygame.draw.polygon(screen, color, pts)
