import pygame

WALL_THICKNESS = 40
DOOR_SIZE = 300


def draw_walls(screen, WIDTH, HEIGHT, room_x, room_y):
    """Rysuje ściany pokoju z dziurami (drzwiami) po środku."""
    color = (100, 100, 100)

    door_x_min = WIDTH // 2 - DOOR_SIZE // 2
    door_x_max = WIDTH // 2 + DOOR_SIZE // 2
    door_y_min = HEIGHT // 2 - DOOR_SIZE // 2
    door_y_max = HEIGHT // 2 + DOOR_SIZE // 2

    # GÓRNA ŚCIANA
    if room_y > 0:
        pygame.draw.rect(screen, color, (0, 0, door_x_min, WALL_THICKNESS))
        pygame.draw.rect(screen, color, (door_x_max, 0, WIDTH - door_x_max, WALL_THICKNESS))
    else:
        pygame.draw.rect(screen, color, (0, 0, WIDTH, WALL_THICKNESS))

    # DOLNA ŚCIANA
    y = HEIGHT - WALL_THICKNESS
    if room_y < 2:
        pygame.draw.rect(screen, color, (0, y, door_x_min, WALL_THICKNESS))
        pygame.draw.rect(screen, color, (door_x_max, y, WIDTH - door_x_max, WALL_THICKNESS))
    else:
        pygame.draw.rect(screen, color, (0, y, WIDTH, WALL_THICKNESS))

    # LEWA ŚCIANA
    if room_x > 0:
        pygame.draw.rect(screen, color, (0, 0, WALL_THICKNESS, door_y_min))
        pygame.draw.rect(screen, color, (0, door_y_max, WALL_THICKNESS, HEIGHT - door_y_max))
    else:
        pygame.draw.rect(screen, color, (0, 0, WALL_THICKNESS, HEIGHT))

    # PRAWA ŚCIANA
    x = WIDTH - WALL_THICKNESS
    if room_x < 2:
        pygame.draw.rect(screen, color, (x, 0, WALL_THICKNESS, door_y_min))
        pygame.draw.rect(screen, color, (x, door_y_max, WALL_THICKNESS, HEIGHT - door_y_max))
    else:
        pygame.draw.rect(screen, color, (x, 0, WALL_THICKNESS, HEIGHT))


def handle_wall_collision(player, WIDTH, HEIGHT, room_x, room_y):
    """
    Jedyna funkcja od ścian:
    - blokuje wchodzenie w ściany
    - pozwala przejść przez drzwi
    - przełącza pokój
    """
    rect = player.rect

    door_x_min = WIDTH // 2 - DOOR_SIZE // 2
    door_x_max = WIDTH // 2 + DOOR_SIZE // 2
    door_y_min = HEIGHT // 2 - DOOR_SIZE // 2
    door_y_max = HEIGHT // 2 + DOOR_SIZE // 2

    # --- LEWA ŚCIANA / przejście do pokoju po lewej ---
    if rect.left < 0:
        if room_x > 0 and door_y_min <= rect.centery <= door_y_max:
            # przejście do pokoju po lewej
            room_x -= 1
            rect.right = WIDTH - 1
        else:
            # blokada o ścianę
            rect.left = 0

    # --- PRAWA ŚCIANA / przejście do pokoju po prawej ---
    if rect.right > WIDTH:
        if room_x < 2 and door_y_min <= rect.centery <= door_y_max:
            room_x += 1
            rect.left = 1
        else:
            rect.right = WIDTH

    # --- GÓRNA ŚCIANA / przejście do pokoju wyżej ---
    if rect.top < 0:
        if room_y > 0 and door_x_min <= rect.centerx <= door_x_max:
            room_y -= 1
            rect.bottom = HEIGHT - 1
        else:
            rect.top = 0

    # --- DOLNA ŚCIANA / przejście do pokoju niżej ---
    if rect.bottom > HEIGHT:
        if room_y < 2 and door_x_min <= rect.centerx <= door_x_max:
            room_y += 1
            rect.top = 1
        else:
            rect.bottom = HEIGHT

    return room_x, room_y
