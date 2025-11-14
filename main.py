import pygame
import sys
import random
from menu import Menu
from player import Player
from objects import ObjectManager
from walls import draw_walls, handle_wall_collision



#from assets import load_textures

WIDTH, HEIGHT = 1920, 1080
FPS = 60
MINIMAP_SIZE = 200
MINIMAP_MARGIN = 20

pygame.init()

#textures = load_textures()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Night Shift")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

menu = Menu(screen, font)
player = Player((WIDTH // 2, HEIGHT // 2))

def draw_minimap(screen, rooms, rx, ry):
    cell = MINIMAP_SIZE // 3
    ox = WIDTH - MINIMAP_SIZE - MINIMAP_MARGIN
    oy = MINIMAP_MARGIN

    for y in range(3):
        for x in range(3):
            r = pygame.Rect(ox + x * cell, oy + y * cell, cell - 3, cell - 3)

            fill = (60, 60, 60) if not rooms[y][x].objects else (90, 90, 130)
            pygame.draw.rect(screen, fill, r)

            border = (255, 255, 0) if (x == rx and y == ry) else (180, 180, 180)
            pygame.draw.rect(screen, border, r, 2)


# ========= ASSETY POKOJÓW – UKŁADY ŚCIAN WEWNĘTRZNYCH =========

def asset_center_room(manager):
    """Kwadratowy mały pokój na środku, z drzwiami na dole."""
    WALL_THICKNESS = 20
    ROOM_WIDTH = WIDTH // 2
    ROOM_HEIGHT = HEIGHT // 2
    DOOR_SIZE = 160

    left = (WIDTH - ROOM_WIDTH) // 2
    top = (HEIGHT - ROOM_HEIGHT) // 2
    right = left + ROOM_WIDTH
    bottom = top + ROOM_HEIGHT

    # drzwi w dolnej ścianie
    door_center_x = WIDTH // 2
    door_left = door_center_x - DOOR_SIZE // 2
    door_right = door_center_x + DOOR_SIZE // 2

    # górna ściana
    manager.objects.append((
        "wall",
        pygame.Rect(left, top, ROOM_WIDTH, WALL_THICKNESS)
    ))
    # lewa ściana
    manager.objects.append((
        "wall",
        pygame.Rect(left, top, WALL_THICKNESS, ROOM_HEIGHT)
    ))
    # prawa ściana
    manager.objects.append((
        "wall",
        pygame.Rect(right - WALL_THICKNESS, top, WALL_THICKNESS, ROOM_HEIGHT)
    ))
    # dolna ściana – z przerwą na drzwi
    if door_left > left:
        manager.objects.append((
            "wall",
            pygame.Rect(left, bottom - WALL_THICKNESS, door_left - left, WALL_THICKNESS)
        ))
    if door_right < right:
        manager.objects.append((
            "wall",
            pygame.Rect(door_right, bottom - WALL_THICKNESS, right - door_right, WALL_THICKNESS)
        ))


def asset_corner_room(manager):
    """Mały pokój w lewym górnym rogu z drzwiami do środka."""
    WALL_THICKNESS = 20
    ROOM_WIDTH = WIDTH // 3
    ROOM_HEIGHT = HEIGHT // 3
    DOOR_SIZE = 120

    left = 120
    top = 120
    right = left + ROOM_WIDTH
    bottom = top + ROOM_HEIGHT

    door_center_x = left + ROOM_WIDTH // 2
    door_left = door_center_x - DOOR_SIZE // 2
    door_right = door_center_x + DOOR_SIZE // 2

    # górna ściana
    manager.objects.append((
        "wall",
        pygame.Rect(left, top, ROOM_WIDTH, WALL_THICKNESS)
    ))
    # lewa ściana
    manager.objects.append((
        "wall",
        pygame.Rect(left, top, WALL_THICKNESS, ROOM_HEIGHT)
    ))
    # prawa ściana
    manager.objects.append((
        "wall",
        pygame.Rect(right - WALL_THICKNESS, top, WALL_THICKNESS, ROOM_HEIGHT)
    ))
    # dolna ściana z drzwiami po środku
    if door_left > left:
        manager.objects.append((
            "wall",
            pygame.Rect(left, bottom - WALL_THICKNESS, door_left - left, WALL_THICKNESS)
        ))
    if door_right < right:
        manager.objects.append((
            "wall",
            pygame.Rect(door_right, bottom - WALL_THICKNESS, right - door_right, WALL_THICKNESS)
        ))


def asset_cross_corridors(manager):
    """Korytarz pionowy i poziomy przecinające się na środku."""
    WALL_THICKNESS = 20
    CORRIDOR_WIDTH = 140

    # pionowy – ściany po bokach korytarza
    corridor_x_left = WIDTH // 2 - CORRIDOR_WIDTH // 2
    corridor_x_right = WIDTH // 2 + CORRIDOR_WIDTH // 2

    manager.objects.append((
        "wall",
        pygame.Rect(0, 0, corridor_x_left, HEIGHT)  # lewa masa ściany
    ))
    manager.objects.append((
        "wall",
        pygame.Rect(corridor_x_right, 0, WIDTH - corridor_x_right, HEIGHT)  # prawa masa ściany
    ))

    # poziomy – znowu zostawiamy pas na korytarz
    corridor_y_top = HEIGHT // 2 - CORRIDOR_WIDTH // 2
    corridor_y_bottom = HEIGHT // 2 + CORRIDOR_WIDTH // 2

    manager.objects.append((
        "wall",
        pygame.Rect(0, 0, WIDTH, corridor_y_top)  # górna masa ściany
    ))
    manager.objects.append((
        "wall",
        pygame.Rect(0, corridor_y_bottom, WIDTH, HEIGHT - corridor_y_bottom)  # dolna masa
    ))


ROOM_ASSETS = [asset_center_room, asset_corner_room, asset_cross_corridors]

# --- Pokoje 3x3 ---
rooms = [[ObjectManager() for _ in range(3)] for _ in range(3)]
room_x, room_y = 1, 2
objects = rooms[room_y][room_x]

# Losowe assety dla każdego pokoju
for ry in range(3):
    for rx in range(3):
        # pomijażeby był pusty:
        # if (rx, ry) == (room_x, room_y):my pokój startowy, jeśli chcesz
        #     continue

        layout_fn = random.choice(ROOM_ASSETS)
        layout_fn(rooms[ry][rx])

# -------- MAIN LOOP --------

running = True
game_started = False

running = True
game_started = False

while running:
    dt = clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_started:
            if menu.handle_event(event) == "start":
                game_started = True
            continue

        # mini-menu
        res = menu.handle_event(event)
        if res in ("triangle", "tall_rect", "long_rect"):
            player.change_shape(res)

        # stawianie obiektów PPM
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            player.place_object(event.pos, objects.objects)

        # --- TU OBSŁUGUJEMY KLAWISZE ---
        if event.type == pygame.KEYDOWN:
            # rotacja kabla
            if event.key == pygame.K_r and player.shape == "long_rect":
                player.rotation = 1 - player.rotation
                if player.rotation == 0:
                    w, h = 80, 25
                else:
                    w, h = 25, 80
                if player.ghost_rect:
                    player.ghost_rect.size = (w, h)

            # USUWANIE obiektu pod myszką
            elif event.key == pygame.K_DELETE and player.shape == "square":
                removed = objects.remove_at_point(mouse_pos)
                # print dla testu:
                # print("Usunięto obiekt?" , removed)

    if game_started:
        keys = pygame.key.get_pressed()
        player.move(keys, objects.objects, WIDTH, HEIGHT)
        player.update(objects.objects)

        # kolizje + ewentualna zmiana pokoju
        prev_x, prev_y = room_x, room_y
        room_x, room_y = handle_wall_collision(player, WIDTH, HEIGHT, room_x, room_y)

        if (room_x, room_y) != (prev_x, prev_y):
            objects = rooms[room_y][room_x]

    # RYSOWANIE
    screen.fill((40, 40, 40))

    if not game_started:
        menu.draw_start_menu(mouse_pos)
    else:
        # --- RYSOWANIE ŚCIAN (NOWOŚĆ) ---
        draw_walls(screen, WIDTH, HEIGHT, room_x, room_y)

        # --- OBIEKTY W POKOJU ---
        powered = objects.compute_powered()
        objects.draw(screen, powered)

        # --- GHOST ---
        can_place = not player.ghost_collides(objects.objects)
        player.draw_ghost(screen, can_place)

        # --- GRACZ & MENU ---
        player.draw(screen)
        menu.draw_mini_menu(mouse_pos)

        # --- MINI MAPA ---
        draw_minimap(screen, rooms, room_x, room_y)

    pygame.display.update()

pygame.quit()
sys.exit()
