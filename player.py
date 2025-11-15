import pygame

# --- SPRITESHEET USTAWIENIA ---
TILE_W = 64
TILE_H = 64

# Ładujemy spritesheet z animacją chodzenia (4 wiersze x 4 kolumny)
# Upewnij się, że plik jest w katalogu "graphics"
sheet = pygame.image.load("graphics/chodzenie_256.png")


def get_frame(col, row):
    """Wytnij jedną klatkę ze spritesheeta."""
    x = col * TILE_W
    y = row * TILE_H
    frame = pygame.Surface((TILE_W, TILE_H), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), (x, y, TILE_W, TILE_H))
    return frame


# 3 klatki animacji na kierunek (kolumny 0–2)
animations = {
    "down":  [get_frame(c, 0) for c in range(3)],
    "right": [get_frame(c, 1) for c in range(3)],
    "up":    [get_frame(c, 2) for c in range(3)],
    "left":  [get_frame(c, 3) for c in range(3)],
}


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, animations, uranek):
        """
        Zgadza się z main.py:
            player = Player(WIDTH // 2, HEIGHT // 2, animations)
        """
        super().__init__()

        # --- ANIMACJA ---
        self.animations = animations
        self.direction = "down"
        self.frame_index = 0
        self.image = self.animations[self.direction][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.uranek = uranek

        # ruch – px / ms (dt z clock.tick(FPS) jest w ms)
        self.speed = 0.3          # ~0.5 px na 1 ms → ~30 px / klatkę przy 60 FPS
        self.anim_speed = 0.01    # "częstotliwość" animacji
        self.anim_timer = 0

        # system kształtów
        self.shape = "square"
        self.shape_sizes = {
            "square":   (TILE_W, TILE_H),  # 64x64
            "triangle": (40, 40),
            "tall_rect": (30, 70),
            "long_rect": (80, 25),
        }
        self.rotation = 0  # 0 = poziomo, 1 = pionowo
        self.ghost_rect: pygame.Rect | None = None

    # ======================= RUCH + ANIMACJA =========================

    def update(self, dt, keys):
        """
        dt – ms z clock.tick(FPS)
        keys – pygame.key.get_pressed()
        """
        vx = vy = 0.0
        new_dir = None

        # sterowanie – UWAGA: keys[...] a nie keys == ...
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

        # ruch (dt w ms → skalujemy)
        self.rect.x += vx * dt
        self.rect.y += vy * dt

        # wybór kierunku dla animacji
        if new_dir and new_dir != self.direction:
            self.direction = new_dir
            self.frame_index = 0
            self.anim_timer = 0

        moving = (vx != 0 or vy != 0)

        # animacja
        if moving:
            self.anim_timer += dt
            # zmiana klatki co ok. 100 ms (1 / 0.01)
            if self.anim_timer >= 1 / self.anim_speed:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
        else:
            self.frame_index = 0  # idle = pierwsza klatka

        self.image = self.animations[self.direction][self.frame_index]

    # ======================= SHAPE (zmiana trybu) =========================

    def change_shape(self, new_shape: str):
        """
        Zmiana trybu: square / triangle / tall_rect / long_rect.
        Sprite gracza się nie zmienia – zmienia się tylko ghost / kształt stawianego obiektu.
        """
        self.shape = new_shape
        # collision box gracza – zawsze square 64x64
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
            else:
                w, h = self.shape_sizes[new_shape]
            self.ghost_rect = pygame.Rect(0, 0, w, h)

    def ghost_collides(self, objects):
        """
        objects – lista krotek (shape, rect),
        czyli objects.objects z ObjectManager.
        """
        if not self.ghost_rect:
            return False

        # 1) kolizja z graczem
        if self.ghost_rect.colliderect(self.rect):
            return True

        # 2) kolizja z obiektami
        for _, r in objects:
            if self.ghost_rect.colliderect(r):
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
                (x + w, y + h),
            ]
            pygame.draw.polygon(screen, color, pts, width=3)
        else:
            pygame.draw.rect(screen, color, self.ghost_rect, width=3)

    # ======================= STAWIANIE OBIEKTÓW =========================

    def place_object(self, mouse_pos, obj_manager):
        """
        obj_manager – instancja ObjectManager (tak jak w main.py: objects)
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
            self.uranek.say("Pamiętaj! Twoje Ręce nie są nieskończenie długie!",3000)
            return

        # kolizja ghosta z obiektami
        if self.ghost_collides(obj_manager.objects):
            return

        # stawianie obiektu
        obj_manager.add_object(self.shape, self.ghost_rect.copy())
        self.change_shape("square")
