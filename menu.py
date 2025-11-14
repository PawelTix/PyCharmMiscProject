import pygame

class Menu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

        # zębatka
        self.gear_rect = pygame.Rect(10, 10, 40, 40)

        # START – niewidzialny przycisk na zielonym "Start" z tła
        # (współczynniki 0.3 / 0.6 / 0.25 / 0.1 możesz potem lekko dostroić)
        sw, sh = screen.get_width(), screen.get_height()
        start_w = int(sw * 0.25)
        start_h = int(sh * 0.10)
        start_x = int(sw * 0.315)
        start_y = int(sh * 0.54)

        self.start_rect = pygame.Rect(0, 0, start_w, start_h)
        self.start_rect.center = (start_x, start_y)

        # opcjonalnie: jeśli chcesz, nadal możesz trzymać napis
        self.start_text = self.font.render("START", True, "white")

        # --- TŁO MENU ---
        # 1) ładujemy oryginalny obraz
        self.bg_img_original = pygame.image.load("graphics/menue_bg.png").convert()

        # 2) skalujemy do rozmiaru ekranu
        sw, sh = self.screen.get_size()
        self.bg_img = pygame.transform.smoothscale(self.bg_img_original, (sw, sh))

        # 3) tło od lewego górnego rogu
        self.bg_rect = self.bg_img.get_rect(topleft=(0, 0))

        # --- MINI MENU ---
        self.buttons = [
            {"label": "Skrzynka energetyczna", "shape": "triangle"},
            {"label": "Generator", "shape": "tall_rect"},
            {"label": "Kabel", "shape": "long_rect"},
        ]
        self.mini_menu_visible = False
        self.mini_buttons = []
        self.create_mini_buttons()

    def create_mini_buttons(self):
        self.mini_buttons.clear()
        x, y = 60, 10
        for btn in self.buttons:
            text = self.font.render(btn["label"], True, "white")
            rect = text.get_rect(topleft=(x + 10, y + 10))
            bg = rect.inflate(20, 10)
            self.mini_buttons.append({
                "shape": btn["shape"],
                "text": text,
                "rect": bg
            })
            y += bg.height + 10

    def draw_start_menu(self, mouse_pos):
        # najpierw tło na cały ekran
        self.screen.blit(self.bg_img, self.bg_rect)



    def draw_mini_menu(self, mouse_pos):
        # zębatka
        pygame.draw.rect(self.screen, (120, 120, 120), self.gear_rect)
        pygame.draw.circle(self.screen, (200, 200, 200), self.gear_rect.center, 15, 3)

        if not self.mini_menu_visible:
            return

        for btn in self.mini_buttons:
            hover = btn["rect"].collidepoint(mouse_pos)
            bg = (120, 120, 120) if hover else (60, 60, 60)
            pygame.draw.rect(self.screen, bg, btn["rect"])
            self.screen.blit(btn["text"], btn["rect"].move(10, 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.start_rect.collidepoint(event.pos):
                return "start"

            # kliknięcia mini-menu
            if self.mini_menu_visible:
                for btn in self.mini_buttons:
                    if btn["rect"].collidepoint(event.pos):
                        self.mini_menu_visible = False
                        return btn["shape"]

            # kliknięcie zębatki
            if self.gear_rect.collidepoint(event.pos):
                self.mini_menu_visible = not self.mini_menu_visible

        return None
