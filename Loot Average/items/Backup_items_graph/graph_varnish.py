import pygame

def get_texture(size):
    surface = pygame.Surface((16, 16), pygame.SRCALPHA).convert_alpha()
    matrix = [
        "......####......", ".....######.....", ".....##..##.....", "....########....",
        "...##########...", "..############..", "..##...##...##..", "..##...##...##..",
        "..##...##...##..", "..############..", "...##########...", "....########....",
        "................", "................", "................"
    ]
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char == '#': surface.set_at((x, y), (140, 80, 40))
            if char == '.': surface.set_at((x, y), (230, 190, 120))
    return pygame.transform.scale(surface, (size, size))
