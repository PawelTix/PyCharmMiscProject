import pygame

class Menu:
    def __init__(self, screen, font):
        self.gear_rect = pygame.Rect(10, 10, 40, 40)
        self.screen = screen
        self.font = font

        # START button
        self.img = pygame.image.load("graphics/menu_bg.png")
        self.start_text = self.font.render("START", True, "white")
        self.start_rect = self.start_text.get_rect(
            center=(
                self.screen.get_width() // 2,
                self.screen.get_height() // 2
            )
        )
        self.bg_rect = self.img.get_rect(
            center=(
                self.screen.get_width() // 2,
                self.screen.get_height() // 2
            )
        )

        # Mini menu buttons
        self.buttons = [
            {"label": "Elektrownia", "shape": "triangle"},
            {"label": "Domek", "shape": "tall_rect"},
            {"label": "Kabel", "shape": "long_rect"},
        ]

        self.mini_buttons = []
        self.mini_menu_visible = False
        self.create_mini_buttons()

    def create_mini_buttons(self):
        """Tworzy przyciski mini menu"""
        self.mini_buttons.clear()
        x, y = 10, 10
        padding = 5

        for btn in self.buttons:
            text = self.font.render(btn["label"], True, "white")
            rect = text.get_rect(topleft=(x + 10, y + 10))
            bg_rect = rect.inflate(20, 10)
            self.mini_buttons.append({
                "label": btn["label"],
                "shape": btn["shape"],
                "text": text,
                "rect": bg_rect
            })
            y += bg_rect.height + padding

    def draw_start_menu(self, mouse_pos):
        """Rysuje ekran startowy"""

        hover = self.start_rect.collidepoint(mouse_pos)
        color = (100, 100, 100) if hover else (50, 50, 50)
        pygame.draw.rect(self.screen, color, self.start_rect.inflate(20, 10))
        self.screen.blit(self.img, self.bg_rect)
        self.screen.blit(self.start_text, self.start_rect)


    def draw_mini_menu(self, mouse_pos):
        pygame.draw.rect(self.screen, (120, 120, 120), self.gear_rect)  # "zębatka"
        pygame.draw.circle(self.screen, (180, 180, 180), self.gear_rect.center, 15, 3)  # efekt koła
        """Rysuje mini menu wyboru kształtu"""
        if not self.mini_menu_visible:
            return

        for btn in self.mini_buttons:
            hover = btn["rect"].collidepoint(mouse_pos)
            color = (120, 120, 120) if hover else (60, 60, 60)
            pygame.draw.rect(self.screen, color, btn["rect"])
            self.screen.blit(btn["text"], btn["rect"].move(10, 5))

    def handle_event(self, event):
        """
        Obsługuje kliknięcia menu.
        Zwraca:
          - "start" gdy kliknięto start
          - nazwę kształtu gracza np. "triangle"
          - None jeśli nic
        """

        if event.type == pygame.MOUSEBUTTONDOWN:

            # Kliknięcie START
            if event.button == 1 and self.start_rect.collidepoint(event.pos):
                return "start"

            if event.button == 1:
                # sprawdzamy czy kliknięto przycisk mini-menu
                clicked_button = False
                if self.mini_menu_visible:
                    for btn in self.mini_buttons:
                        if btn["rect"].collidepoint(event.pos):
                            clicked_button = True
                            self.mini_menu_visible = False
                            return btn["shape"]
                # Kliknięcie w zębatkę otwiera / zamyka mini menu
                if self.gear_rect.collidepoint(event.pos):
                    self.mini_menu_visible = not self.mini_menu_visible
            if self.mini_menu_visible:
                mini_menu_area = pygame.Rect(60, 10, 150, len(self.mini_buttons) * 50)
                if not mini_menu_area.collidepoint(event.pos) and not self.gear_rect.collidepoint(event.pos):
                    self.mini_menu_visible = False

        return None
