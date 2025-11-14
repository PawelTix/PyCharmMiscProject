import pygame

class Player:
    def __init__(self, start_pos):
        self.x, self.y = start_pos
        self.speed = 5
        self.rotation = 0  # 0 = poziomo, 1 = pionowo

        # rozmiary kształtów
        self.shape_sizes = {
            "square": (40, 40),
            "triangle": (40, 40),
            "tall_rect": (30, 70),
            "long_rect": (80, 25)
        }

        self.shape = "square"
        self.rect = pygame.Rect(self.x, self.y, *self.shape_sizes["square"])

        self.ghost_rect = None

    # ======================= RUCH =========================

    def move(self, keys, objects, W, H):
        dx = dy = 0
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed

        old = self.rect.copy()

        self.rect.x += dx
        for _, r in objects:
            if self.rect.colliderect(r):
                self.rect = old
                return

        old = self.rect.copy()
        self.rect.y += dy
        for _, r in objects:
            if self.rect.colliderect(r):
                self.rect = old
                return

    # ======================= SHAPE =========================

    def change_shape(self, new_shape):
        self.shape = new_shape
        # gracz jako gracz zawsze square
        self.rect.size = self.shape_sizes["square"]

        if new_shape == "square":
            self.ghost_rect = None
        else:
            if new_shape == "long_rect":
                # uwzględniamy rotację (0 = poziom, 1 = pion)
                if self.rotation == 0:
                    w, h = 80, 25
                else:
                    w, h = 25, 80
                self.ghost_rect = pygame.Rect(0, 0, w, h)
            else:
                w, h = self.shape_sizes[new_shape]
                self.ghost_rect = pygame.Rect(0, 0, w, h)

    def update(self):
        """Ghost podąża za myszką."""
        if self.ghost_rect:
            mx, my = pygame.mouse.get_pos()
            self.ghost_rect.center = (mx, my)

    def ghost_collides(self, objects):
        """Sprawdza, czy ghost nachodzi na gracza ALBO na inne obiekty."""
        if not self.ghost_rect:
            return False

        # 1) kolizja z graczem
        if self.ghost_rect.colliderect(self.rect):
            return True

        # 2) kolizja z innymi obiektami
        for _, r in objects:
            if self.ghost_rect.colliderect(r):
                return True

        return False

    # ======================= RYSOWANIE =========================

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 200, 255), self.rect)

    def draw_ghost(self, screen, ok):
        if not self.ghost_rect:
            return
        color = (0, 255, 0) if ok else (255, 0, 0)

        if self.shape == "triangle":
            x, y, w, h = self.ghost_rect
            pts = [
                (x + w // 2, y),
                (x, y + h),
                (x + w, y + h)
            ]
            pygame.draw.polygon(screen, color, pts, width=3)
        else:
            pygame.draw.rect(screen, color, self.ghost_rect, width=3)

    # ======================= STAWIANIE =========================

    def place_object(self, mouse_pos, objects):
        if self.shape == "square":
            return
        if not self.ghost_rect:
            return
        if self.ghost_collides(objects):
            return

        objects.append((self.shape, self.ghost_rect.copy()))
        self.change_shape("square")
