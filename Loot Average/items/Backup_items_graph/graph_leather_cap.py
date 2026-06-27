import pygame

def get_texture(size):
    surface = pygame.Surface((16, 16), pygame.SRCALPHA).convert_alpha()
    matrix = [
        ".....CCCCCC.....", "...CCLLLLLLCC...", "..CLLLLLLLLLLC..", ".CLLGGGGGGLLLLC.",
        ".CLLCLLLLCLLLLC.", "CLLLCLLLLCLLLLLC", "CLL........LLLLC", "CC..........CCC"
    ]
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char == 'C': surface.set_at((x, y), (30, 20, 15))    # 1. Черный контур
            if char == 'L': surface.set_at((x, y), (120, 75, 35))   # 2. Темная кожа
            if char == 'G': surface.set_at((x, y), (55, 135, 110))  # 3. Зеленый узор
    surface.set_at((6, 2), (185, 135, 85))                          # 4. Светлый блик
    surface.set_at((7, 2), (185, 135, 85))
    return pygame.transform.scale(surface, (size, size))
