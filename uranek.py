import pygame
import textwrap


class Uranek:
    def __init__(self, screen_rect: pygame.Rect):
        # Spróbuj załadować grafikę uranka
        try:
            # wrzuć sobie np. assets/uranek.png albo graphics/uranek.png
            self.image = pygame.image.load("assets/uranek_maly.png").convert_alpha()
        except Exception:
            # Fallback – jak nie ma pliku, rysujemy prostą kapsułkę
            self.image = pygame.Surface((120, 140), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, (50, 200, 50), (10, 20, 100, 120))
            pygame.draw.circle(self.image, (0, 0, 0), (60, 55), 8)   # oko 1
            pygame.draw.circle(self.image, (0, 0, 0), (85, 60), 8)   # oko 2
            pygame.draw.arc(self.image, (0, 0, 0), (40, 70, 60, 40), 3.3, 6.0, 3)

        self.rect = self.image.get_rect()
        # prawy dolny róg z marginesem
        margin = 20
        self.rect.bottomright = (screen_rect.width - margin, screen_rect.height - margin)

        # Tekst / dymek
        self.font = pygame.font.SysFont("consolas", 20)
        self.text = ""
        self.visible = False
        self.timer = 0
        self.duration = 0

        # parametry dymka
        self.bubble_max_width = 320
        self.bubble_padding = 10

    def say(self, text: str, duration_ms: int = 5000):
        """Uranek mówi coś przez określony czas (w ms)."""
        self.text = text
        self.duration = duration_ms
        self.timer = 0
        self.visible = True

    def update(self, dt_ms: int):
        """dt_ms – to samo dt, którego używasz w main (z clock.tick)."""
        if not self.visible:
            return
        self.timer += dt_ms
        if self.timer >= self.duration:
            self.visible = False

    def _render_bubble(self, screen: pygame.Surface):
        if not self.text:
            return

        # zawijanie linii
        words = self.text.split()
        lines = []
        current = ""

        for w in words:
            test = (current + " " + w).strip()
            surf = self.font.render(test, True, (0, 0, 0))
            if surf.get_width() > self.bubble_max_width and current:
                lines.append(current)
                current = w
            else:
                current = test
        if current:
            lines.append(current)

        # rozmiar dymka
        line_surfs = [self.font.render(l, True, (0, 0, 0)) for l in lines]
        width = max(s.get_width() for s in line_surfs) + 2 * self.bubble_padding
        height = sum(s.get_height() for s in line_surfs) + 2 * self.bubble_padding

        # dymek nad urankiem
        bubble_rect = pygame.Rect(0, 0, width, height)
        bubble_rect.right = self.rect.left - 10
        bubble_rect.bottom = self.rect.bottom

        # tło dymka
        bubble_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(bubble_surf, (0, 0, 0, 180), bubble_surf.get_rect(), border_radius=12)
        inner_rect = bubble_surf.get_rect().inflate(-4, -4)
        pygame.draw.rect(bubble_surf, (180, 255, 180), inner_rect, border_radius=10)

        # tekst w środku
        y = self.bubble_padding
        for s in line_surfs:
            bubble_surf.blit(s, (self.bubble_padding, y))
            y += s.get_height()

        screen.blit(bubble_surf, bubble_rect.topleft)

        # mały „ogon” dymka
        p1 = (bubble_rect.right, bubble_rect.bottom - 20)
        p2 = (bubble_rect.right + 12, bubble_rect.bottom - 10)
        p3 = (bubble_rect.right, bubble_rect.bottom - 5)
        pygame.draw.polygon(screen, (0, 0, 0, 180), [p1, p2, p3])
        pygame.draw.polygon(screen, (180, 255, 180), [p1, (p2[0] - 3, p2[1]), p3])

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        # najpierw dymek, potem sprite
        self._render_bubble(screen)
        screen.blit(self.image, self.rect)
