import pygame

def get_texture(size):
    surface = pygame.Surface((16, 16), pygame.SRCALPHA).convert_alpha()
    p_matrix = [
        "......####......", "......####......", ".....######.....", "....########....",
        "....#..##..#....", "...#...##...#...", "..#....##....#..", "..#..######..#..",
        "..#..######..#..", "..#..######..#..", "..#..######..#..", "...#........#...",
        "....########....", ".....######.....", "................", "................"
    ]
    for y, row in enumerate(p_matrix):
        for x, char in enumerate(row):
            if char == '#': surface.set_at((x, y), (240, 240, 255)) # Белое стекло
            if char == '.': surface.set_at((x, y), (210, 30, 30))   # Красная жидкость
    # Белый медицинский крест
    surface.set_at((7, 8), (255, 255, 255))
    surface.set_at((8, 8), (255, 255, 255))
    surface.set_at((7, 9), (255, 255, 255))
    surface.set_at((8, 9), (255, 255, 255))
    surface.set_at((6, 9), (255, 255, 255))
    surface.set_at((9, 9), (255, 255, 255))
    return pygame.transform.scale(surface, (size, size))
