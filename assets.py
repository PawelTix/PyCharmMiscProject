import pygame
import os

ASSETS_FOLDER = "assets"

# mapowanie "typu obiektu" na nazwę pliku
SPRITE_FILES = {
    "triangle":  "powerplant.png",  # elektrownia
    "tall_rect": "house.png",       # domek
    "long_rect": "cable.png",       # kabel
}


def load_image(filename: str) -> pygame.Surface:
    """Ładuje jeden obrazek z katalogu assets/ i zwraca Surface."""
    path = os.path.join(ASSETS_FOLDER, filename)
    img = pygame.image.load(path).convert_alpha()
    return img


def load_textures() -> dict:
    """
    Stare API – zwraca słownik z gołymi Surface’ami.
    Możesz z tego nadal korzystać, jeśli gdzieś w kodzie używasz samych tekstur.
    """
    return {name: load_image(fname) for name, fname in SPRITE_FILES.items()}


def create_sprite(kind: str, pos=(0, 0)) -> pygame.sprite.Sprite:
    """
    Tworzy sprite’a danego typu:
      kind ∈ {"player", "triangle", "tall_rect", "long_rect"}

    Sprite ma pola:
      - image  (Surface)
      - rect   (pygame.Rect) – wycentrowany w podanym `pos`
      - kind   (string z typem obiektu)
    """
    if kind not in SPRITE_FILES:
        raise ValueError(f"Nieznany typ sprite'a: {kind}")

    image = load_image(SPRITE_FILES[kind])

    sprite = pygame.sprite.Sprite()
    sprite.image = image
    sprite.rect = image.get_rect(center=pos)
    sprite.kind = kind
    return sprite


# Wygodne funkcje pomocnicze – możesz używać zamiast create_sprite(...)
def create_player(pos=(0, 0)) -> pygame.sprite.Sprite:
    return create_sprite("player", pos)


def create_powerplant(pos=(0, 0)) -> pygame.sprite.Sprite:
    return create_sprite("triangle", pos)


def create_house(pos=(0, 0)) -> pygame.sprite.Sprite:
    return create_sprite("tall_rect", pos)


def create_cable(pos=(0, 0)) -> pygame.sprite.Sprite:
    return create_sprite("long_rect", pos)
