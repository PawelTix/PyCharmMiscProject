import pygame
import sys
from menu import Menu
from player import Player
from objects import ObjectManager
from cables import CableManager

# --- Ustawienia ---
WIDTH, HEIGHT = 1920, 1080
FPS = 60
MINIMAP_SIZE = 200   # była 120 – teraz większa
MINIMAP_MARGIN = 20  # odstęp od prawej/górnej krawędzi
cable_mgr = CableManager(max_conn_distance=80)  # dostosuj do długości long_rect

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modularna Gra Pygame")
clock = pygame.time.Clock()

# fonty
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

# --- Moduły ---
menu = Menu(screen, font)
player = Player(start_pos=(WIDTH // 2, HEIGHT // 2))

# --- Pokoje 3x3 ---
# rooms[y][x] = ObjectManager dla danego pokoju
rooms = [[ObjectManager() for _ in range(3)] for _ in range(3)]

# zaczynamy w środkowym pokoju (1,1)
# zaczynamy w dolnym środkowym pokoju (1,2)
room_x, room_y = 1, 2
objects = rooms[room_y][room_x]

# Aktualizujemy listę kabli na podstawie obiektów w aktualnym pokoju
cable_mgr.sync_from_objects(objects.objects)

# Źródła prądu i odbiorniki (później to zmienisz na swoje typy)
power_sources = [obj for obj in objects.objects if getattr(obj, "kind", "") == "power_plant"]
consumers = [obj for obj in objects.objects if getattr(obj, "kind", "") == "house"]

# Propagacja prądu
cable_mgr.update_power_state(power_sources, consumers)


game_started = False

def draw_minimap(screen, rooms, current_x, current_y):
    """Rysuje mini-mapę 3x3 w prawym górnym rogu."""
    cell_size = MINIMAP_SIZE // 3
    # lewy górny róg mini-mapy
    mini_x = WIDTH - MINIMAP_SIZE - MINIMAP_MARGIN
    mini_y = MINIMAP_MARGIN

    for ry in range(3):          # ry = indeks w pionie (wiersz)
        for rx in range(3):      # rx = indeks w poziomie (kolumna)
            x = mini_x + rx * cell_size
            y = mini_y + ry * cell_size
            rect = pygame.Rect(x, y, cell_size - 2, cell_size - 2)

            # kolor wnętrza pokoju
            if rooms[ry][rx].objects:
                fill_color = (90, 90, 130)   # pokój z obiektami
            else:
                fill_color = (60, 60, 60)    # pusty pokój

            pygame.draw.rect(screen, fill_color, rect)

            # ramka – żółta dla aktualnego pokoju, szara dla innych
            if rx == current_x and ry == current_y:
                border_color = (255, 255, 0)   # aktualny pokój
                border_width = 3
            else:
                border_color = (180, 180, 180)
                border_width = 1

            pygame.draw.rect(screen, border_color, rect, border_width)

# --- Główna pętla ---
running = True
while running:

    dt = clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    # --- Obsługa zdarzeń ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- MENU STARTU ---
        if not game_started:
            result = menu.handle_event(event)
            if result == "start":
                game_started = True
            # dopóki jesteśmy w menu startu, nie obsługujemy niczego więcej
            continue

        # --- GRA (mini-menu + stawianie obiektów) ---
        result = menu.handle_event(event)
        if result in ["triangle", "tall_rect", "long_rect"]:
            player.change_shape(result)

        # PPM – stawianie obiektów
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            player.place_object(event.pos, objects.objects)

    # --- LOGIKA GRY ---
    if game_started:
        keys = pygame.key.get_pressed()
        player.move(keys, objects.objects, WIDTH, HEIGHT)
        player.update()  # ghost podąża za myszką

        # --- Przejścia między pokojami (3x3) ---
        # używamy elif, żeby w jednym kroku przechodzić tylko przez jedną ścianę
        if player.rect.left <= 0 and room_x > 0:
            # przejście do pokoju po lewej
            room_x -= 1
            objects = rooms[room_y][room_x]
            player.rect.right = WIDTH - 10  # pojawiamy się przy prawej krawędzi

        elif player.rect.right >= WIDTH and room_x < 2:
            # przejście do pokoju po prawej
            room_x += 1
            objects = rooms[room_y][room_x]
            player.rect.left = 10  # pojawiamy się przy lewej krawędzi

        elif player.rect.top <= 0 and room_y > 0:
            # przejście do pokoju wyżej
            room_y -= 1
            objects = rooms[room_y][room_x]
            player.rect.bottom = HEIGHT - 10  # pojawiamy się przy dolnej krawędzi

        elif player.rect.bottom >= HEIGHT and room_y < 2:
            # przejście do pokoju niżej
            room_y += 1
            objects = rooms[room_y][room_x]
            player.rect.top = 10  # pojawiamy się przy górnej krawędzi
            # 🔌 aktualizacja kabli w tym pokoju

        cable_mgr.sync_from_objects(objects.objects)

        power_sources = [obj for obj in objects.objects if getattr(obj, "kind", "") == "power_plant"]
        consumers = [obj for obj in objects.objects if getattr(obj, "kind", "") == "house"]

        cable_mgr.update_power_state(power_sources, consumers)
    # --- RYSOWANIE ---
    screen.fill((50, 50, 50))  # tło

    if not game_started:
        # ekran startowy
        menu.draw_start_menu(mouse_pos)
    else:
        # obiekty w aktualnym pokoju
        objects.draw(screen)

        # ghost (podgląd obiektu)
        can_place = not player.ghost_collides(objects.objects)
        player.draw_ghost(screen, can_place)

        # gracz + mini-menu
        player.draw(screen)
        menu.draw_mini_menu(mouse_pos)

        # mały napis z numerem pokoju (1–3 zamiast 0–2)
        if not game_started:
            menu.draw_start_menu(mouse_pos)
        else:
            objects.draw(screen)

            # ghost (podgląd obiektu)
            can_place = not player.ghost_collides(objects.objects)
            player.draw_ghost(screen, can_place)

            # gracz + mini-menu
            player.draw(screen)
            menu.draw_mini_menu(mouse_pos)

            # mini-mapa 3x3
            draw_minimap(screen, rooms, room_x, room_y)

    pygame.display.update()

pygame.quit()
sys.exit()
