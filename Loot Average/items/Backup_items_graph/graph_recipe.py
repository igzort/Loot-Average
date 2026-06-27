import pygame

def get_texture(size):
    surface = pygame.Surface((16, 16), pygame.SRCALPHA).convert_alpha()
    matrix = [
        "....########....", "...##########...", "..##..####..##..", "..#.########.#..",
        "..#..###..##.#..", "..#..####...##..", "..#..#######.#..", "..#..##..###.#..",
        "..#..##...##.#..", "..#.####..##.#..", "..##..####..##..", "...##########...",
        "....########...."
    ]
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char == '#': surface.set_at((x, y), (235, 235, 225)) # Бумага
            if char == '.': surface.set_at((x, y), (40, 40, 45))     # Чернила "R"
    return pygame.transform.scale(surface, (size, size))
