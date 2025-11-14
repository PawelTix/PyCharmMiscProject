import pygame

class ObjectManager:
    def __init__(self):
        # lista postawionych obiektów w formie: (shape, rect)
        self.objects = []

    def add_object(self, shape, rect):
        """Dodaje nowy obiekt na mapę"""
        self.objects.append((shape, rect.copy()))

    def draw(self, screen):
        """Rysuje wszystkie obiekty"""
        for shape, rect in self.objects:
            if shape == "square" or shape == "tall_rect" or shape == "long_rect":
                pygame.draw.rect(screen, (40, 40, 200), rect)
            elif shape == "triangle":
                px, py, pw, ph = rect
                points = [
                    (px + pw // 2, py),      # top
                    (px, py + ph),           # bottom left
                    (px + pw, py + ph)       # bottom right
                ]
                pygame.draw.polygon(screen, (40, 40, 200), points)

    def check_collision(self, rect):
        """Sprawdza kolizję podanego prostokąta z obiektami"""
        for _, obj_rect in self.objects:
            if rect.colliderect(obj_rect):
                return True
        return False
