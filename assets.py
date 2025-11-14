import pygame
import os

ASSETS_FOLDER = "assets"


def load_image(filename):
    """Ładuje jeden obrazek z assets/"""
    path = os.path.join(ASSETS_FOLDER, filename)
    img = pygame.image.load(path).convert_alpha()
    return img


def load_textures():
    """Ładuje wszystkie tekstury gry jako słownik."""
    textures = {
        "player":    load_image("player.png"),       # Player
        "triangle":  load_image("powerplant.png"),   # elektrownia
        "tall_rect": load_image("house.png"),        # domek
        "long_rect": load_image("cable.png"),        # kabel
    }
    return textures
