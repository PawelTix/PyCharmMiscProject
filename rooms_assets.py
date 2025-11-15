import pygame
import random
from generator_spawns import generator_spawns
# === MAŁY HELPER, KTÓREGO BRAKUJE ===
def _add_wall(manager, rect: pygame.Rect):
    manager.add_wall(rect)

def third_map_asset(manager, width, height, room_x, room_y):
    WALL = 20

    left   = 0
    right  = width
    top    = 0
    bottom = height

    W = right - left
    H = bottom - top

    # Kluczowe proporcje odwzorowane z rysunku
    x_left_inner  = int(0.28 * W)   # pionowa lewa wewnętrzna
    x_mid_short   = int(0.64 * W)   # środkowa pionowa krótka
    x_right_inner = int(0.78 * W)   # pionowa prawa

    y_mid_h1      = int(0.3 * H)   # górna wewnętrzna pozioma
    y_mid_h2      = int(0.67 * H)   # dolna wewnętrzna pozioma
    y_bottom_short= int(0.87 * H)   # pionowa dolna krótka

    # ==== LEWA WEWNĘTRZNA PIONOWA ====
    _add_wall(manager, pygame.Rect(
        x_left_inner, top,
        WALL, int(0.5 * H)
    ))

    # ==== POZIOMA ZE ŚRODKA LEWEJ PIONOWEJ ====
    _add_wall(manager, pygame.Rect(
        x_left_inner, y_mid_h1,
        int(0.3 * W), WALL
    ))

    # ==== LEWA KRÓTKA POZIOMA (drzwi) ====
    _add_wall(manager, pygame.Rect(
        left, y_mid_h2,
        int(0.2 * W), WALL
    ))

    # ==== DUŻA ŚRODKOWA POZIOMA ====
    _add_wall(manager, pygame.Rect(
        x_left_inner, y_mid_h2,
        x_right_inner - x_left_inner, WALL
    ))

    # ==== KRÓTKA PIONOWA ZE ŚRODKA POZIOMEJ ====
    _add_wall(manager, pygame.Rect(
        x_mid_short, y_mid_h2,
        WALL, int(0.18 * H)
    ))

    # ==== DOLNA PIONOWA KRÓTKA ====
    _add_wall(manager, pygame.Rect(
        int(0.35 * W), y_bottom_short,
        WALL, bottom - y_bottom_short
    ))

    # ==== PRAWA POZIOMA KRÓTKA (drzwi) ====
    _add_wall(manager, pygame.Rect(
        x_right_inner, y_mid_h1,
        int(0.1 * W), WALL
    ))

    # ==== PRAWA PIONOWA Z DRZWIAMI NA WYSOKOŚCI y_mid_h2 ====
    door_height = int(0.12* H)  # wysokość otworu drzwi
    door_center = y_mid_h2 +100  # środek drzwi = pozioma ściana
    door_top = door_center - door_height // 2
    door_bottom = door_top + door_height

    # górny kawałek prawej ściany
    if door_top > top:
        _add_wall(manager, pygame.Rect(
            x_right_inner,
            top,
            WALL,
            door_top - top
        ))

    # dolny kawałek prawej ściany
    if bottom > door_bottom:
        _add_wall(manager, pygame.Rect(
            x_right_inner,
            door_bottom,
            WALL,
            bottom - door_bottom
        ))

        # ================== MIEJSCA NA GENERATORY ==================
        # przykładowo: jedno bardziej po lewej u góry, drugie po prawej na dole

        spot1 = (int(0.25 * width), int(0.30 * height))
        spot2 = (int(0.70 * width), int(0.75 * height))

        generator_spawns.set_spots((room_x, room_y), [spot1, spot2])

def second_map_asset(manager, width, height, room_x, room_y):
    WALL = 20

    left   = 0
    right  = width
    top    = 0
    bottom = height

    W = right - left
    H = bottom - top

    # poprawione proporcje
    x_left_inner   = int(0.35 * W)   # lewa pionowa ściana
    x_stub         = int(0.70 * W)   # pionowa odnoga z poziomej  (bardziej w lewo!)
    x_vertical_mid = int(0.7 * W)   # dolna pionowa po prawej   (bardziej w prawo!)
    x_right_short  = int(0.87 * W)   # krótka pozioma przy prawej ścianie

    y_horizontal   = int(0.31* H)   # główna pozioma ściana
    y_bottom_line  = int(0.68 * H)   # dolne poziome
    y_vert_top     = int(0.55 * H)   # start dolnej pionowej
    stub_height    = int(0.13 * H)

    # --- lewa pionowa ---
    _add_wall(manager, pygame.Rect(
        x_left_inner, top,
        WALL, y_bottom_line - top
    ))

    # --- dwa dolne poziome w lewym pokoju ---

    seg1_end = int(0.18 * W)
    _add_wall(manager, pygame.Rect(
        left, y_bottom_line,
        seg1_end - left, WALL
    ))

    seg2_start = int(0.26 * W)
    _add_wall(manager, pygame.Rect(
        seg2_start, y_bottom_line,
        x_left_inner - seg2_start, WALL
    ))

    # --- główna pozioma ---
    _add_wall(manager, pygame.Rect(
        x_left_inner, y_horizontal,
        x_stub - x_left_inner, WALL
    ))

    # --- pionowa odnoga (L-ka) ---
    _add_wall(manager, pygame.Rect(
        x_stub, y_horizontal,
        WALL, stub_height
    ))

    # --- krótka pozioma przy prawej ---
    _add_wall(manager, pygame.Rect(
        x_right_short, y_horizontal,
        right - x_right_short, WALL
    ))

    # --- dolna pionowa po prawej ---
    _add_wall(manager, pygame.Rect(
        x_vertical_mid, y_vert_top,
        WALL, bottom - y_vert_top
    ))

    # ================== MIEJSCA NA GENERATORY ==================
    # przykładowo: jedno bardziej po lewej u góry, drugie po prawej na dole

    spot1 = (int(0.383 * width), int(0.265 * height))
    spot2 = (int(0.05 * width), int(0.80 * height))

    generator_spawns.set_spots((room_x, room_y), [spot1, spot2])

def first_map_asset(manager, width, height, room_x, room_y):
    """
    Układ inspirowany szkicem:
    - dwa pokoje po lewej u góry z przerwą na drzwi
    - pionowa ściana schodząca ze środka w dół
    - po prawej pionowa ściana z poziomą belką i pionową odnogą
    - dwie pionowe ścianki w dolnej części (skrócone = drzwi)
    """
    WALL = 20

    # BEZ marginesu – wewnętrzne ściany mogą stykać się z zewnętrznymi
    left   = 0
    right  = width
    top    = 0
    bottom = height

    W = right - left
    H = bottom - top

    mid_x = (left + right) // 2

    # Poziom mniej więcej w 1/3 wysokości
    y_top_inner = int(top + 0.30 * H)

    # piony ~ tak jak na rysunku
    x_left_inner  = int(left + 0.30 * W)   # lewy wewnętrzny
    x_right_inner = int(left + 0.70 * W)   # prawy wewnętrzny

    # ---- GÓRNA LEWA CZĘŚĆ ----

    # krótka pozioma ściana od lewej ściany do okolic 1/5 szerokości
    h1_end = int(left + 0.20 * W)
    _add_wall(manager, pygame.Rect(
        left,
        y_top_inner,
        h1_end - left,
        WALL
    ))

    # przerwa = drzwi

    # druga krótka pozioma ściana bliżej środka, dochodząca do x_left_inner
    # h2_start MUSI być < x_left_inner
    h2_start = int(left + 0.28 * W)   # 0.24W < 0.30W
    _add_wall(manager, pygame.Rect(
        h2_start,
        y_top_inner,
        x_left_inner - h2_start,
        WALL
    ))

    # pionowa ściana schodząca z końca tej poziomej w dół (nie do samego dołu)
    y_mid_down = int(top + 0.65 * H)
    _add_wall(manager, pygame.Rect(
        x_left_inner,
        y_top_inner,
        WALL,
        y_mid_down - y_top_inner
    ))

    # ---- PIONY W GÓRZE ----

    # lewy wewnętrzny pion – od górnej krawędzi do poziomej
    _add_wall(manager, pygame.Rect(
        x_left_inner,
        top,
        WALL,
        y_top_inner - top
    ))

    # prawy wewnętrzny pion – z DRZWIAMI
    door_height_main = int(0.12 * H)            # wysokość otworu
    door_center_main = int(top + 0.55 * H)      # położenie drzwi (środek)

    door_top_main = max(top + 10, door_center_main - door_height_main // 2)
    door_bottom_main = min(bottom - 10, door_top_main + door_height_main)

    # górny fragment ściany
    if door_top_main > top:
        _add_wall(manager, pygame.Rect(
            x_right_inner,
            top,
            WALL,
            door_top_main - top
        ))

    # dolny fragment ściany
    if bottom > door_bottom_main:
        _add_wall(manager, pygame.Rect(
            x_right_inner,
            door_bottom_main,
            WALL,
            bottom - door_bottom_main
        ))

    # ---- PRAWY „KORYTARZ” ----

    # pozioma ściana pod postacią – z DRZWIAMI pośrodku
    y_corridor = int(top + 0.68 * H)
    span = right - x_right_inner
    door_width = int(0.3 * span)  # było 0.18, teraz większe drzwi
    door_width = max(50, min(door_width, span - 30))

    door_left = x_right_inner + (span - door_width) // 2
    door_right = door_left + door_width

    # lewy kawałek ściany
    if door_left > x_right_inner:
        _add_wall(manager, pygame.Rect(
            x_right_inner,
            y_corridor,
            door_left - x_right_inner,
            WALL
        ))

    # prawy kawałek ściany
    if right > door_right:
        _add_wall(manager, pygame.Rect(
            door_right,
            y_corridor,
            right - door_right,
            WALL
        ))

    # ---- DÓŁ ----

    # pionowa ścianka na dole po lewej stronie tej dolnej części – też skrócona od dołu
    x_bottom_right = left + int(0.30 * W)
    y_bottom_right_top = int(top + 0.80 * H)
    door_clearance2 = int(0.05 * H)
    y_bottom_right_end = bottom - door_clearance2

    _add_wall(manager, pygame.Rect(
        x_bottom_right,
        y_bottom_right_top,
        WALL,
        y_bottom_right_end - y_bottom_right_top
    ))

    # ================== MIEJSCA NA GENERATORY ==================
    # przykładowo: jedno bardziej po lewej u góry, drugie po prawej na dole


    spot1 = (int(0.26 * width), int(0.05 * height))
    spot2 = (int(0.70 * width), int(0.75 * height))
    generator_spawns.set_spots((room_x, room_y), [spot1,spot2])

ROOM_ASSETS = [first_map_asset, second_map_asset, third_map_asset]


def apply_random_room_assets(rooms, width, height, skip=None):
    if skip is None:
        skip = set()

    for ry in range(len(rooms)):
        for rx in range(len(rooms[0])):
            if (rx, ry) in skip:
                continue
            layout_fn = random.choice(ROOM_ASSETS)
            layout_fn(rooms[ry][rx], width, height, rx, ry)
