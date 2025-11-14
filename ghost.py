import pygame

SNAP_RADIUS = 35  # promień przyciągania do końców kabli


def _get_cable_endpoints(rect: pygame.Rect):
    """Zwraca dwa punkty na końcach kabelka (krótszy bok = miejsce łączenia)."""
    x, y, w, h = rect

    if w >= h:  # kabel poziomy
        return [
            (x, y + h // 2),           # lewy koniec
            (x + w, y + h // 2)        # prawy koniec
        ]
    else:       # kabel pionowy
        return [
            (x + w // 2, y),           # górny koniec
            (x + w // 2, y + h)        # dolny koniec
        ]


def update_ghost(player, objects):
    """
    Aktualizuje pozycję ghosta:
    - zawsze podąża za myszką
    - dla kabelków ('long_rect') przyciąga się do końców innych kabli

    objects – lista sprite’ów (GameObject) z ObjectManager.objects
    """
    if not player.ghost_rect:
        return

    mx, my = pygame.mouse.get_pos()
    # 1. ghost leci za myszką
    player.ghost_rect.center = (mx, my)

    # 2. snap tylko dla kabla
    if player.shape != "long_rect":
        return

    nearest_point = None
    nearest_dist2 = SNAP_RADIUS * SNAP_RADIUS

    # szukamy najbliższego punktu złącza na istniejących kablach
    for obj in objects:
        shape = obj.kind
        rect = obj.rect

        if shape != "long_rect":
            continue

        for cx, cy in _get_cable_endpoints(rect):
            dx = mx - cx
            dy = my - cy
            d2 = dx * dx + dy * dy
            if d2 < nearest_dist2:
                nearest_dist2 = d2
                nearest_point = (cx, cy)

    if nearest_point is None:
        return  # za daleko od jakiegokolwiek złącza

    cx, cy = nearest_point

    # sprawdzamy, którą końcówkę naszego ghosta lepiej przyczepić
    ghost_points = _get_cable_endpoints(player.ghost_rect)

    best_rect = None
    best_dist2 = None

    for ex, ey in ghost_points:
        dx = cx - ex
        dy = cy - ey

        candidate = player.ghost_rect.copy()
        candidate.move_ip(dx, dy)

        c_cx, c_cy = candidate.center
        ddx = c_cx - mx
        ddy = c_cy - my
        d2 = ddx * ddx + ddy * ddy

        if best_dist2 is None or d2 < best_dist2:
            best_dist2 = d2
            best_rect = candidate

    if best_rect is not None:
        player.ghost_rect = best_rect
