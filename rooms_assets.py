import pygame
import random


def asset_center_room(manager, width, height):
    """Kwadratowy mały pokój na środku, z drzwiami na dole."""
    WALL_THICKNESS = 20
    ROOM_WIDTH = width // 2
    ROOM_HEIGHT = height // 2
    DOOR_SIZE = 160

    left = (width - ROOM_WIDTH) // 2
    top = (height - ROOM_HEIGHT) // 2
    right = left + ROOM_WIDTH
    bottom = top + ROOM_HEIGHT

    door_center_x = width // 2
    door_left = door_center_x - DOOR_SIZE // 2
    door_right = door_center_x + DOOR_SIZE // 2

    manager.add_wall(pygame.Rect(left, top, ROOM_WIDTH, WALL_THICKNESS))               # góra
    manager.add_wall(pygame.Rect(left, top, WALL_THICKNESS, ROOM_HEIGHT))              # lewo
    manager.add_wall(pygame.Rect(right - WALL_THICKNESS, top, WALL_THICKNESS, ROOM_HEIGHT))  # prawo

    # dół z przerwą na drzwi
    if door_left > left:
        manager.add_wall(pygame.Rect(left, bottom - WALL_THICKNESS,
                                     door_left - left, WALL_THICKNESS))
    if door_right < right:
        manager.add_wall(pygame.Rect(door_right, bottom - WALL_THICKNESS,
                                     right - door_right, WALL_THICKNESS))


def asset_corner_room(manager, width, height):
    """Mały pokój w lewym górnym rogu z drzwiami do środka."""
    WALL_THICKNESS = 20
    ROOM_WIDTH = width // 3
    ROOM_HEIGHT = height // 3
    DOOR_SIZE = 120

    left = 120
    top = 120
    right = left + ROOM_WIDTH
    bottom = top + ROOM_HEIGHT

    door_center_x = left + ROOM_WIDTH // 2
    door_left = door_center_x - DOOR_SIZE // 2
    door_right = door_center_x + DOOR_SIZE // 2

    manager.add_wall(pygame.Rect(left, top, ROOM_WIDTH, WALL_THICKNESS))                # góra
    manager.add_wall(pygame.Rect(left, top, WALL_THICKNESS, ROOM_HEIGHT))               # lewo
    manager.add_wall(pygame.Rect(right - WALL_THICKNESS, top, WALL_THICKNESS, ROOM_HEIGHT))  # prawo

    # dół z drzwiami
    if door_left > left:
        manager.add_wall(pygame.Rect(left, bottom - WALL_THICKNESS,
                                     door_left - left, WALL_THICKNESS))
    if door_right < right:
        manager.add_wall(pygame.Rect(door_right, bottom - WALL_THICKNESS,
                                     right - door_right, WALL_THICKNESS))


def asset_cross_corridors(manager, width, height):
    """Korytarz pionowy i poziomy przecinające się na środku."""
    WALL_THICKNESS = 20
    CORRIDOR_WIDTH = 140

    cx_left = width // 2 - CORRIDOR_WIDTH // 2
    cx_right = width // 2 + CORRIDOR_WIDTH // 2
    cy_top = height // 2 - CORRIDOR_WIDTH // 2
    cy_bottom = height // 2 + CORRIDOR_WIDTH // 2

    # pion – duże bloki po bokach
    manager.add_wall(pygame.Rect(0, 0, cx_left, height))
    manager.add_wall(pygame.Rect(cx_right, 0, width - cx_right, height))

    # poziom – bloki nad i pod
    manager.add_wall(pygame.Rect(0, 0, width, cy_top))
    manager.add_wall(pygame.Rect(0, cy_bottom, width, height - cy_bottom))


ROOM_ASSETS = [asset_center_room, asset_corner_room, asset_cross_corridors]


def apply_random_room_assets(rooms, width, height, skip=None):
    if skip is None:
        skip = set()

    for ry in range(len(rooms)):
        for rx in range(len(rooms[0])):
            if (rx, ry) in skip:
                continue
            layout_fn = random.choice(ROOM_ASSETS)
            layout_fn(rooms[ry][rx], width, height)
