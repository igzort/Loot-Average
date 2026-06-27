# sprites.py
import pygame
import config as cfg
import os

class SpriteGenerator:
    def __init__(self):
        self.mob_size = int(cfg.WIDTH * 0.40)
        self.all_textures = self._generate_all()

    def _generate_all(self):
        tex = {}
        project_root = os.path.dirname(os.path.abspath(__file__))
        mobs_list = ["Wolf", "Werewolf", "Orc Grunt"]
        
        for mob_name in mobs_list:
            # Массив возможных вариантов названия картинки на диске
            possible_files = [
                f"{mob_name}.png",                      # "Orc Grunt.png"
                f"{mob_name.lower()}.png",              # "orc grunt.png"
                f"{mob_name.replace(' ', '_')}.png",    # "Orc_Grunt.png"
                f"{mob_name.lower().replace(' ', '_')}.png" # "orc_grunt.png"
            ]
            
            path = None
            for filename in possible_files:
                check_path = os.path.join(project_root, "assets", "mobs", filename)
                if os.path.exists(check_path):
                    path = check_path
                    break # Как только нашли совпадение — берём его
            
            if path and os.path.exists(path):
                # 1. Загружаем реальную найденную картинку
                img = pygame.image.load(path).convert_alpha()
                # 2. Сжимаем до 32х32 (жесткий пиксель-арт без размытия)
                small_img = pygame.transform.scale(img, (32, 32))
                # 3. Растягиваем до игрового размера экрана
                tex[mob_name] = pygame.transform.scale(small_img, (self.mob_size, self.mob_size))
            else:
                # ЗАПАСНОЙ ВАРИАНТ (Если вообще ни один файл не найден)
                fallback = pygame.Surface((16, 16), pygame.SRCALPHA).convert_alpha()
                if mob_name == "Wolf":
                    w_matrix = [
                        "................", "......###.......", "....#######.....", "...#########....",
                        "..##########....", "..#.########....", "....########....", "....#########...",
                        "....##########..", "....##########..", "....##########..", "....##..##..##..",
                        "....##..##..##..", "....#...#...#...", "....#...#...#...", "................"
                    ]
                    for y, row in enumerate(w_matrix):
                        for x, char in enumerate(row):
                            if char == '#': fallback.set_at((x, y), (140, 145, 150))
                elif mob_name == "Werewolf":
                    ww_matrix = [
                        "......####......", "....########....", "...##########...", "..############..",
                        "..###..#######..", "..#..#.#######..", ".....#########..", "....##########..",
                        "....##########..", "....##########..", "..#############.", "..##..##..##..##",
                        "....##..##..##..", "....#...#...#...", "....#...#...#...", "................"
                    ]
                    for y, row in enumerate(ww_matrix):
                        for x, char in enumerate(row[:16]):
                            if char == '#': fallback.set_at((x, y), (90, 80, 95))
                else:
                    fallback.fill((50, 120, 50)) # Зелёный орк
                
                tex[mob_name] = pygame.transform.scale(fallback, (self.mob_size, self.mob_size))
                
        return tex
