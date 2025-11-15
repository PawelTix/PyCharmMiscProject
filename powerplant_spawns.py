# powerplant_spawns.py

class PowerplantSpawnSystem:
    """
    Trzyma informacje, w jakich punktach danego pokoju
    mogą pojawić się generatory (triangle).
    Dla każdego pokoju np. 2 lokacje [(x1, y1), (x2, y2)].
    """

    def __init__(self):
        # (room_x, room_y) -> lista [(x, y), (x, y), ...]
        self.spots_by_room: dict[tuple[int, int], list[tuple[int, int]]] = {}

    def set_spots(self, room_pos, spots):
        """
        room_pos: (room_x, room_y)
        spots: lista [(x, y), ...] – np. 2 lokacje w pokoju
        """
        self.spots_by_room[tuple(room_pos)] = list(spots)

    def get_spots(self, room_pos):
        """
        Zwraca listę [(x, y)] dla pokoju lub [] jeśli nic nie zarejestrowano.
        """
        return self.spots_by_room.get(tuple(room_pos), [])


# globalna instancja, jak przy generator_spawns / electric_doors
powerplant_spawns = PowerplantSpawnSystem()
