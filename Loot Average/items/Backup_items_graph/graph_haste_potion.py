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
            if char == '#': surface.set_at((x, y), (150, 150, 160))
            if char == '.': surface.set_at((x, y), (30, 144, 255))
    return pygame.transform.scale(surface, (size, size))
