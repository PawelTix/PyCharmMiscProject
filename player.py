import pygame

TILE_W = 64
TILE_H = 64

sheet = pygame.image.load("graphics/chodzenie_256.png")


def get_frame(col, row):
    x = col * TILE_W
    y = row * TILE_H
    frame = pygame.Surface((TILE_W, TILE_H), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), (x, y, TILE_W, TILE_H))
    return frame


animations = {
    "down": [get_frame(c, 0) for c in range(3)],
    "right": [get_frame(c, 1) for c in range(3)],
    "up": [get_frame(c, 2) for c in range(3)],
    "left": [get_frame(c, 3) for c in range(4)],
}


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, animations):


        # --- SPRITE (obrazek gracza) ---
        # Na razie prostokąt – możesz tu później podmienić na swój spritesheet.
        super().__init__()
        self.animations = animations
        self.direction = "down"
        self.frame_index = 0
        self.image = self.animations[self.direction][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.ghost_rect: pygame.Rect | None = None
        self.speed = 1  # px/s
        self.anim_speed = 8  # klatek na sekundę
        self.anim_timer = 0
        self.shape = "square"
        self.shape_sizes = {
            "square": (40, 40),
            "triangle": (40, 40),
            "tall_rect": (30, 70),
            "long_rect": (80, 25)
        }
        self.rotation = 0

        # ======================= RUCH =========================

    def update(self, dt, keys):
        vx = vy = 0
        new_dir = None

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vy = -self.speed
            new_dir = "up"
        elif keys==pygame.K_s or keys==pygame.K_DOWN:
            vy = self.speed
            new_dir = "down"
        if keys==pygame.K_a or keys==pygame.K_LEFT:
            vx = -self.speed
            new_dir = "left"
        elif keys==pygame.K_d or keys==pygame.K_RIGHT:
            vx = self.speed
            new_dir = "right"

        # ruch
        self.rect.x += vx * dt
        self.rect.y += vy * dt

        # wybór kierunku
        if new_dir:
            if new_dir != self.direction:
                self.direction = new_dir
                self.frame_index = 0  # reset animacji

        moving = (vx != 0 or vy != 0)

        # animacja
        if moving:
            self.anim_timer += dt
            if self.anim_timer >= 1 / self.anim_speed:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
        else:
            self.frame_index = 0  # pierwsza klatka jako idle

        self.image = self.animations[self.direction][self.frame_index]

    # ======================= SHAPE =========================

    def update(self, dt, keys):
        vx = vy = 0
        new_dir = None

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vy = -self.speed
            new_dir = "up"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            vy = self.speed
            new_dir = "down"
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            vx = -self.speed
            new_dir = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            vx = self.speed
            new_dir = "right"

        # ruch
        self.rect.x += vx * dt
        self.rect.y += vy * dt

        # wybór kierunku
        if new_dir:
            if new_dir != self.direction:
                self.direction = new_dir
                self.frame_index = 0  # reset animacji

        moving = (vx != 0 or vy != 0)

        # animacja
        if moving:
            self.anim_timer += dt
            if self.anim_timer >= 1 / self.anim_speed:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
        else:
            self.frame_index = 0  # pierwsza klatka jako idle

        self.image = self.animations[self.direction][self.frame_index]

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

    # ======================= STAWIANIE =========================

    def place_object(self, mouse_pos, obj_manager):
        """
        Stawia obiekt przez ObjectManager.
        obj_manager – instancja ObjectManager (nie lista!).
        """
        # nie stawiamy jeśli gracz w trybie square


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