import pygame

def get_texture(size):
    surface = pygame.Surface((16, 16), pygame.SRCALPHA).convert_alpha()
    matrix = [
        "......####......", "....########....", "...##########...", "..############..",
        "..###..##..###..", ".####..##..####.", ".####..##..####.", ".####..##..####.",
        ".####..##..####.", ".####..##..####.", "..###..##..###..", "..############..",
        "...##########...", "....########....", "......####......", "................"
    ]
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char == '#': surface.set_at((x, y), (255, 215, 0))
            if char == '.': surface.set_at((x, y), (180, 130, 20))
    return pygame.transform.scale(surface, (size, size))
