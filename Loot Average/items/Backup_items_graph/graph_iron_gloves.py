import pygame

def get_texture(size):
    surface = pygame.Surface((16, 16), pygame.SRCALPHA).convert_alpha()
    g_matrix = [
        "................", "....####.####...", "....####.####...", "....#########...",
        "....#########...", "....##.###.##...", "....#########...", "................"
    ]
    for y, row in enumerate(g_matrix):
        for x, char in enumerate(row):
            if char == '#': surface.set_at((x, y), (180, 185, 190))
    return pygame.transform.scale(surface, (size, size))
