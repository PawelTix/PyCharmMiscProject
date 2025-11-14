import pygame
from collections import deque
from assets import load_textures


class ObjectManager:
    def __init__(self):
        # lista: (shape, rect)
        self.objects = []

        # wczytujemy wszystkie tekstury z assets/
        # klucze: "player", "triangle", "tall_rect", "long_rect"
        self.textures = load_textures()

        # cache przeskalowanych sprite’ów, żeby nie skalować co klatkę
        # klucz: (shape, width, height) -> Surface
        self._scaled_cache = {}

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
            if shape == "wall":
                continue  # NIE pozwalamy usuwać ścian
            if rect.collidepoint(x, y):
                del self.objects[i]
                return True
        return False

    def compute_powered(self):
        """Zwraca indeksy obiektów, które mają połączenie z elektrownią (triangle)."""
        n = len(self.objects)
        if n == 0:
            return set()

        # Znajdź elektrownie
        power_plants = [i for i, (shape, _) in enumerate(self.objects)
                        if shape == "triangle"]
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

    # =================== POMOCNICZE – SPRITE Z PIXEL ARTU ===================

    def _get_sprite_image(self, shape, size):
        """Zwraca przeskalowany obrazek dla danego shape i size lub None."""
        w, h = size
        key = (shape, w, h)

        if key in self._scaled_cache:
            return self._scaled_cache[key]

        base_img = self.textures.get(shape)
        if base_img is None:
            return None  # brak tekstury – użyjemy fallbacku (kolorowy rect)

        scaled = pygame.transform.smoothscale(base_img, (w, h))
        self._scaled_cache[key] = scaled
        return scaled

    # =================== RYSOWANIE ===================

    def draw(self, screen, powered=None):
        if powered is None:
            powered = set()

        # --- najpierw ściany (żeby były pod obiektami) ---
        for shape, rect in self.objects:
            if shape == "wall":
                pygame.draw.rect(screen, (80, 80, 80), rect)  # szara ściana

        # --- potem wszystkie obiekty (triangle / tall_rect / long_rect) ---
        for idx, (shape, rect) in enumerate(self.objects):
            if shape == "wall":
                continue

            # spróbuj narysować pixel-art
            img = self._get_sprite_image(shape, rect.size)

            if img is not None:
                screen.blit(img, rect)

                # podświetlenie, jeśli ma prąd
                if idx in powered:
                    pygame.draw.rect(screen, (0, 255, 0), rect, 3)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)
                continue

            # --- Fallback: gdyby brakło tekstury, rysujemy stary prostokąt ---

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
