import pygame

class Player:
    def __init__(self, start_pos=(400, 300), speed=5):
        # domyślny kształt
        self.shape = "square"
        self.speed = speed
        self.ghost_rect = None
        self.default_size = 50

        # rozmiary dla każdego kształtu
        self.shape_sizes = {
            "square": (40, 40),
            "triangle": (40, 40),
            "tall_rect": (30, 70),
            "long_rect": (80, 25)
        }

        self.rect = pygame.Rect(0, 0, *self.shape_sizes[self.shape])
        self.rect.center = start_pos

    def move(self, keys, placed_objects, screen_width, screen_height):
        """Ruch gracza z kolizjami"""

        dx = dy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed

        if dx != 0 or dy != 0:
            old_rect = self.rect.copy()
            self.rect.x += dx
            self.rect.y += dy
            self.clamp(screen_width, screen_height)

            if self.check_collision(placed_objects):
                self.rect = old_rect

    def clamp(self, width, height):
        """Blokuje wyjście poza ekran"""
        self.rect.x = max(0, min(width - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(height - self.rect.height, self.rect.y))

    def check_collision(self, placed_objects):
        """Sprawdza kolizje z postawionymi obiektami"""
        for _, obj_rect in placed_objects:
            if self.rect.colliderect(obj_rect):
                return True
        return False

    def change_shape(self, new_shape):
        """Zmienia kształt gracza i przygotowuje ghosta, jeśli to obiekt do postawienia."""
        self.shape = new_shape

        # dopasowanie rozmiaru prostokąta gracza (dla kolizji itd.)
        if new_shape in self.shape_sizes:
            self.rect.size = self.shape_sizes[new_shape]

        # KWADRAT = tryb gracza → nie pokazujemy podglądu
        if new_shape == "square":
            self.ghost_rect = None
        else:
            # dla elektrowni, domku, kabla tworzymy prostokąt ghosta
            w, h = self.shape_sizes[new_shape]
            self.ghost_rect = pygame.Rect(0, 0, w, h)

    def place_object(self, mouse_pos, placed_objects):
        # jeśli kształt to square → nic nie stawiamy
        if self.shape == "square":
            return

        # jeśli ghost nie istnieje → nic nie rób
        if not self.ghost_rect:
            return

        # jeśli ghost koliduje
        if self.ghost_collides(placed_objects):
            print("❌ Nie możesz postawić obiektu tutaj!")
            return

        # stawiamy obiekt na pozycji ghosta
        placed_objects.append((self.shape, self.ghost_rect.copy()))

        # wracamy do kwadratu
        self.change_shape("square")

    def draw(self, screen, color=(200, 40, 40)):
        """Rysuje gracza na ekranie"""
        if self.shape == "square" or self.shape == "tall_rect" or self.shape == "long_rect":
            pygame.draw.rect(screen, color, self.rect)
        elif self.shape == "triangle":
            px, py, pw, ph = self.rect
            points = [
                (px + pw // 2, py),      # top
                (px, py + ph),           # bottom left
                (px + pw, py + ph)       # bottom right
            ]
            pygame.draw.polygon(screen, color, points)

    def draw_ghost(self, screen, can_place: bool):
        """Rysuje podgląd obiektu (ghost) – trójkąt lub prostokąt, w kolorze zależnym od kolizji."""
        if not self.ghost_rect:
            return

        # kolor ramki
        color = (0, 255, 0) if can_place else (255, 0, 0)

        # prostokątne kształty
        if self.shape in ("square", "tall_rect", "long_rect"):
            pygame.draw.rect(screen, color, self.ghost_rect, width=3)

        # trójkąt – elektrownia
        elif self.shape == "triangle":
            x, y = self.ghost_rect.x, self.ghost_rect.y
            w, h = self.ghost_rect.width, self.ghost_rect.height

            points = [
                (x + w // 2, y),        # góra
                (x, y + h),             # dół lewo
                (x + w, y + h)          # dół prawo
            ]

            pygame.draw.polygon(screen, color, points, width=3)

    def update(self):
        """Aktualizuje pozycję ghosta tak, żeby podążał za myszką."""
        if self.ghost_rect:
            mouse_pos = pygame.mouse.get_pos()
            self.ghost_rect.center = mouse_pos

    def ghost_collides(self, placed_objects):
        """Sprawdza, czy ghost nachodzi na gracza albo na inne obiekty."""
        if not self.ghost_rect:
            return False

        # kolizja z graczem
        if self.ghost_rect.colliderect(self.rect):
            return True

        # kolizja z innymi obiektami
        for _, obj_rect in placed_objects:
            if self.ghost_rect.colliderect(obj_rect):
                return True

        return False
