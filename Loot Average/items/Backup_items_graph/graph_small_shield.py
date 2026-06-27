import pygame

def get_texture(size):
    surface = pygame.Surface((16, 16), pygame.SRCALPHA).convert_alpha()
    matrix = [
        "......####......", "....########....", "...##########...", "..############..",
        "..############..", ".##############.", ".##############.", ".##############.",
        ".##############.", "..############..", "..############..", "...##########...",
        "....########....", "......####......"
    ]
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char == '#': surface.set_at((x, y), (140, 85, 35))   # 1. Бронза центра
            if char == '.': surface.set_at((x, y), (225, 185, 80))  # 2. Золотой кант
    surface.set_at((7, 4), (85, 45, 15))                            # 3. Темно-бронзовая тень
    surface.set_at((8, 4), (85, 45, 15))
    surface.set_at((5, 4), (255, 255, 240))                         # 4. Яркий белый блик
    return pygame.transform.scale(surface, (size, size))
