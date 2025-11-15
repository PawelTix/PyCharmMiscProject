import pygame

# Możesz je zsynchronizować z plikiem, w którym masz draw_walls:
WALL_THICKNESS = 40
DOOR_SIZE = 300


class ElectricDoorSystem:
    """
    Steruje drzwiami między pokojami w siatce (room_x, room_y).
    Każdy pokój ma 4 drzwi: left, right, up, down.
    Jeśli pokój jest "zasilony" -> wszystkie drzwi się otwierają.
    """

    def __init__(self, grid_w: int, grid_h: int):
        self.grid_w = grid_w
        self.grid_h = grid_h
        # domyślnie wszystkie drzwi zamknięte
        self._open = {}  # (x,y) -> dict(dir->bool)

    def _ensure_room(self, room_x: int, room_y: int):
        key = (room_x, room_y)
        if key not in self._open:
            self._open[key] = {
                "left": False,
                "right": False,
                "up": False,
                "down": False,
            }
        return self._open[key]

    # ---------- API zasilania pokoju ----------

    def set_room_powered(self, room_x: int, room_y: int, powered: bool):
        """
        Jeśli powered == True -> wszystkie drzwi pokoju są otwarte.
        Jeśli False -> wszystkie zamknięte.
        """
        state = self._ensure_room(room_x, room_y)
        for k in state.keys():
            state[k] = powered

    # ---------- Kolizja ze ścianami zewnętrznymi + drzwi ----------

    def handle_collision(self, player, WIDTH, HEIGHT, room_x: int, room_y: int):
        """
        Zastępuje stare handle_wall_collision:
        - blokuje ściany zewnętrzne
        - pozwala przejść przez drzwi TYLKO gdy są otwarte
        - przełącza room_x, room_y
        """
        rect = player.rect
        door_x_min = WIDTH // 2 - DOOR_SIZE // 2
        door_x_max = WIDTH // 2 + DOOR_SIZE // 2
        door_y_min = HEIGHT // 2 - DOOR_SIZE // 2
        door_y_max = HEIGHT // 2 + DOOR_SIZE // 2

        state = self._ensure_room(room_x, room_y)

        # --- LEWA ŚCIANA / przejście do pokoju po lewej ---
        if rect.left < 0:
            if room_x > 0 and state["left"] and door_y_min <= rect.centery <= door_y_max:
                # drzwi otwarte -> przejście do sąsiedniego pokoju
                room_x -= 1
                rect.right = WIDTH - 1
            else:
                # brak drzwi lub zamknięte -> ściana
                rect.left = 0

        # --- PRAWA ŚCIANA / przejście do pokoju po prawej ---
        if rect.right > WIDTH:
            if room_x < self.grid_w - 1 and state["right"] and door_y_min <= rect.centery <= door_y_max:
                room_x += 1
                rect.left = 1
            else:
                rect.right = WIDTH

        # --- GÓRNA ŚCIANA / przejście do pokoju wyżej ---
        if rect.top < 0:
            if room_y > 0 and state["up"] and door_x_min <= rect.centerx <= door_x_max:
                room_y -= 1
                rect.bottom = HEIGHT - 1
            else:
                rect.top = 0

        # --- DOLNA ŚCIANA / przejście do pokoju niżej ---
        if rect.bottom > HEIGHT:
            if room_y < self.grid_h - 1 and state["down"] and door_x_min <= rect.centerx <= door_x_max:
                room_y += 1
                rect.top = 1
            else:
                rect.bottom = HEIGHT

        return room_x, room_y


# globalny system, żeby łatwo importować
electric_doors = ElectricDoorSystem(grid_w=3, grid_h=3)  # jeśli masz 3x3 pokoje
