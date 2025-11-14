import pygame

class Menu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

        # zębatka
        self.gear_rect = pygame.Rect(10, 10, 40, 40)

        # START
        self.start_text = self.font.render("START", True, "white")
        self.start_rect = self.start_text.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2)
        )
        self.bg_img = pygame.image.load("graphics/menue_bg.png")
        self.bg_rect = self.bg_img.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2)
        )

        # mini menu
        self.buttons = [
            {"label": "Generator", "shape": "triangle"},
            {"label": "Energia", "shape": "tall_rect"},
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
        hover = self.start_rect.collidepoint(mouse_pos)
        color = (150, 150, 150) if hover else (100, 100, 100)
        pygame.draw.rect(self.screen, color, self.start_rect.inflate(30, 20))
        self.screen.blit(self.bg_img, self.bg_rect)
        self.screen.blit(self.start_text, self.start_rect)

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
