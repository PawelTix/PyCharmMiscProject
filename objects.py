import pygame
from collections import deque


class ObjectManager:
    def __init__(self):
        self.objects = []  # lista: (shape, rect)

    def add_object(self, shape, rect):
        self.objects.append((shape, rect.copy()))

    # =================== LOGIKA POŁĄCZEŃ ===================

    def _rect_connected(self, r1, r2):
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

    def remove_at_point(self, pos):
        x, y = pos
        for i in range(len(self.objects) - 1, -1, -1):
            shape, rect = self.objects[i]
            if rect.collidepoint(x, y):
                del self.objects[i]
                return True
        return False

        return False

    def compute_powered(self):
        """Zwraca indeksy obiektów, które mają połączenie z elektrownią (triangle)."""
        n = len(self.objects)
        if n == 0:
            return set()

        # Znajdź elektrownie
        power_plants = [i for i, (shape, _) in enumerate(self.objects) if shape == "triangle"]
        if not power_plants:
            return set()

        # Budujemy graf połączeń
        adj = [[] for _ in range(n)]
        for i in range(n):
            si, ri = self.objects[i]
            if si not in ("triangle", "tall_rect", "long_rect"):
                continue

            for j in range(i + 1, n):
                sj, rj = self.objects[j]
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

        for idx, (shape, rect) in enumerate(self.objects):
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
