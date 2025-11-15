import pygame
import sys
import random
from menu import Menu
from player import Player, animations
from objects import ObjectManager
from walls import draw_walls
from rooms_assets import apply_random_room_assets
from ghost import update_ghost
from uranek import Uranek
from electric_doors import ElectricDoorSystem
#from assets import load_textures


WIDTH, HEIGHT = 1080, 700
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

# --- URANEK ---
uranek = Uranek(screen.get_rect())

menu = Menu(screen, font)
pygame.mixer_music.load("muzyka/dzwiek menu.mp3")
player = Player(WIDTH // 2, HEIGHT // 2, animations,uranek)
electric_doors = ElectricDoorSystem(uranek, grid_w=3, grid_h=3)

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

# --- Pokoje 3x3 ---
rooms = [[ObjectManager() for _ in range(3)] for _ in range(3)]
room_x, room_y = 1, 2
objects = rooms[room_y][room_x]

# losowe układy ścian wewnętrznych
apply_random_room_assets(rooms, WIDTH, HEIGHT, skip={(room_x, room_y)})

# -------- MAIN LOOP --------

running = True
game_started = False

running = True
game_started = False
pygame.mixer.music.play(-1)
while running:
    dt = clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_started:
            if menu.handle_event(event) == "start":
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load("muzyka/dzwiek pokoju1.mp3")
                pygame.mixer.music.play(-1)
                game_started = True
                uranek.say("Cześć! Jestem Uranek.\nMusisz podłączyć generatory do szkrzynek elektrycznych używając kabli, aby otworzyć przejście do kolejnego pokoju.", 6000)
            continue

        # mini-menu
        res = menu.handle_event(event)
        if res in ("triangle", "tall_rect", "long_rect"):
            if res == "triangle":
                uranek.say("postaw generator")
            elif res == "tall_rect":
                uranek.say("postaw skrzynke")
            elif res == "long_rect":
                uranek.say("postaw kabel")
            player.change_shape(res)

        # stawianie obiektów PPM
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            player.place_object(event.pos, objects)

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

    current_manager = rooms[room_y][room_x]
    powered_indices = current_manager.compute_powered()
    objs = current_manager.objects

    generator_powered = False
    for i in powered_indices:
        if 0 <= i < len(objs):
            obj = objs[i]

            # spróbuj wziąć typ z atrybutu .kind
            kind = getattr(obj, "kind", None)

            # jeśli to krotka typu ("tall_rect", rect, ...) – weź pierwszy element
            if kind is None and isinstance(obj, tuple) and len(obj) > 0:
                kind = obj[0]

            if kind == "tall_rect":
                generator_powered = True
                break

    electric_doors.set_room_powered(room_x, room_y, generator_powered)

    if game_started:
        keys = pygame.key.get_pressed()
        player.update(dt, keys)
        update_ghost(player, objects.objects)
        uranek.update(dt)

        # kolizje + ewentualna zmiana pokoju
        prev_x, prev_y = room_x, room_y

        room_x, room_y = electric_doors.handle_collision(player, WIDTH, HEIGHT, room_x, room_y)

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

        # --- URANEK PODPOWIADA ---
        uranek.draw(screen)

    pygame.display.update()

pygame.quit()
sys.exit()
