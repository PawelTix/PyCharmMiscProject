import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()

        # --- SPRITE (obrazek gracza) ---
        # Na razie prostokąt – możesz tu później podmienić na swój spritesheet.
        size = (40, 40)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill((0, 200, 255))  # kolor gracza

        self.rect = self.image.get_rect(center=start_pos)

        self.speed = 5
        self.rotation = 0  # 0 = poziomo, 1 = pionowo

        # rozmiary kształtów do stawiania obiektów
        self.shape_sizes = {
            "square": (40, 40),
            "triangle": (40, 40),
            "tall_rect": (30, 70),
            "long_rect": (80, 25)
        }

        self.shape = "square"
        self.ghost_rect: pygame.Rect | None = None

    # ======================= RUCH =========================

    def move(self, keys, objects, W, H):
        """
        objects – lista sprite’ów obiektów (GameObject) w aktualnym pokoju.
        Kolizje sprawdzamy po rectach.
        """
        dx = dy = 0
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed

        # ruch X
        old = self.rect.copy()
        self.rect.x += dx
        for obj in objects:
            r = obj.rect
            if self.rect.colliderect(r):
                self.rect = old
                return

        # ruch Y
        old = self.rect.copy()
        self.rect.y += dy
        for obj in objects:
            r = obj.rect
            if self.rect.colliderect(r):
                self.rect = old
                return

    # ======================= SHAPE =========================

    def change_shape(self, new_shape: str):
        """
        Zmiana trybu: square/triangle/tall_rect/long_rect.
        Gracz wizualnie dalej jest kwadratem, ale ghost ma inny kształt.
        """
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

    def ghost_collides(self, objects):
        """Sprawdza, czy ghost nachodzi na gracza ALBO na inne obiekty."""
        if not self.ghost_rect:
            return False

        # 1) kolizja z graczem
        if self.ghost_rect.colliderect(self.rect):
            return True

        # 2) kolizja z innymi obiektami
        for obj in objects:
            if self.ghost_rect.colliderect(obj.rect):
                return True

        return False

    # ======================= RYSOWANIE =========================

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_ghost(self, screen, ok: bool):
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

    def place_object(self, mouse_pos, obj_manager):
        """
        Stawia obiekt przez ObjectManager.
        obj_manager – instancja ObjectManager (nie lista!).
        """
        # nie stawiamy jeśli gracz w trybie square
        if self.shape == "square":
            return

        if not self.ghost_rect:
            return

        # --- LIMIT ZASIĘGU ---
        px, py = self.rect.center
        mx, my = mouse_pos
        dx = mx - px
        dy = my - py
        MAX_PLACE_DISTANCE = 250

        if dx * dx + dy * dy > MAX_PLACE_DISTANCE * MAX_PLACE_DISTANCE:
            print("❌ Za daleko aby postawić obiekt!")
            return

        # kolizja ghosta
        if self.ghost_collides(obj_manager.objects):
            return

        # stawianie
        obj_manager.add_object(self.shape, self.ghost_rect.copy())
        self.change_shape("square")