import pygame

def get_texture(size):
    surface = pygame.Surface((16, 16), pygame.SRCALPHA).convert_alpha()
    for i in range(16):
        surface.set_at((15 - i, i), (139, 69, 19))      # 1. Дерево основы
        surface.set_at((14 - i, i), (205, 133, 63))     # 2. Светлый блик дерева
        surface.set_at((i, i), (220, 220, 220, 150))    # 3. Тетива
    surface.set_at((15, 0), (192, 192, 192))            # 4. Железный наконечник
    surface.set_at((0, 15), (192, 192, 192))            # 4. Железный наконечник 2
    return pygame.transform.scale(surface, (size, size))
