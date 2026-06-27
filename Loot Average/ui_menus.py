# ui_menus.py
import pygame
import config as cfg

class UIMenus:
    def __init__(self, core):
        self.core = core

    def draw_mobs(self, screen, logic):
        w, h = cfg.WIDTH, cfg.HEIGHT
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0,0))
        
        pygame.draw.rect(screen, cfg.MODAL_BG, self.core.menu_mobs_bg, border_radius=8)
        pygame.draw.rect(screen, cfg.UI_BORDER, self.core.menu_mobs_bg, 2, border_radius=8)
        screen.blit(self.core.font_big.render("SELECT TARGET:", True, cfg.TEXT_COLOR), (int(w * 0.08), int(h * 0.22)))
        
        pygame.draw.rect(screen, cfg.RESET_COLOR, self.core.btn_close_mobs, border_radius=4)
        screen.blit(self.core.font_small.render("CLOSE", True, cfg.TEXT_COLOR), (self.core.btn_close_mobs.centerx - 20, self.core.btn_close_mobs.centery - 7))

        # 1. Волк (Wolf)
        w_color = cfg.ACTIVE_TAB if logic.current_mob_type == "Wolf" else cfg.INACTIVE_TAB
        pygame.draw.rect(screen, w_color, self.core.row_wolf_rect, border_radius=4)
        screen.blit(self.core.font_small.render("Lv.4 Wolf", True, cfg.TEXT_COLOR), (int(w * 0.12), int(h * 0.295)))
        pygame.draw.rect(screen, cfg.BTN_DROP, self.core.drop_wolf_rect, border_radius=4)
        screen.blit(self.core.font_small.render("DROP", True, cfg.DROP_COLOR), (self.core.drop_wolf_rect.centerx - 14, self.core.drop_wolf_rect.centery - 7))

        # 2. Вервольф (Werewolf)
        ww_color = cfg.ACTIVE_TAB if logic.current_mob_type == "Werewolf" else cfg.INACTIVE_TAB
        pygame.draw.rect(screen, ww_color, self.core.row_ww_rect, border_radius=4)
        screen.blit(self.core.font_small.render("Lv.9 Werewolf", True, cfg.TEXT_COLOR), (int(w * 0.12), int(h * 0.375)))
        pygame.draw.rect(screen, cfg.BTN_DROP, self.core.drop_ww_rect, border_radius=4)
        screen.blit(self.core.font_small.render("DROP", True, cfg.DROP_COLOR), (self.core.drop_ww_rect.centerx - 14, self.core.drop_ww_rect.centery - 7))

        # 3. Орк (Orc Grunt)
        step_y = self.core.row_ww_rect.y - self.core.row_wolf_rect.y
        self.core.row_orc_rect = self.core.row_ww_rect.move(0, step_y)
        self.core.drop_orc_rect = self.core.drop_ww_rect.move(0, step_y)
        
        orc_color = cfg.ACTIVE_TAB if logic.current_mob_type == "Orc Grunt" else cfg.INACTIVE_TAB
        pygame.draw.rect(screen, orc_color, self.core.row_orc_rect, border_radius=4)
        screen.blit(self.core.font_small.render("Lv.7 Orc Grunt", True, cfg.TEXT_COLOR), (int(w * 0.12), int(h * 0.375) + step_y))
        pygame.draw.rect(screen, cfg.BTN_DROP, self.core.drop_orc_rect, border_radius=4)
        screen.blit(self.core.font_small.render("DROP", True, cfg.DROP_COLOR), (self.core.drop_orc_rect.centerx - 14, self.core.drop_orc_rect.centery - 7))

    def draw_drop(self, screen, logic):
        w, h = cfg.WIDTH, cfg.HEIGHT
        pygame.draw.rect(screen, cfg.MODAL_BG, self.core.menu_drop_bg, border_radius=8)
        pygame.draw.rect(screen, cfg.DROP_COLOR, self.core.menu_drop_bg, 1, border_radius=8)
        
        tgt_mob = logic.show_droplist_for
        screen.blit(self.core.font_big.render(f"{tgt_mob} Drop:", True, cfg.DROP_COLOR), (int(w * 0.14), int(h * 0.27)))
        
        pygame.draw.rect(screen, cfg.RESET_COLOR, self.core.btn_close_drop, border_radius=4)
        screen.blit(self.core.font_small.render("BACK", True, cfg.TEXT_COLOR), (self.core.btn_close_drop.centerx - 16, self.core.btn_close_drop.centery - 7))
        
        mob_m = cfg.MOBS_DATA[tgt_mob]
        dy, step_y = int(h * 0.33), max(14, int(h * 0.020))
        
        # Задаем фиксированную правую границу для столбца процентов (с отступом от правого края золотой рамки)
        right_align_x = int(w * 0.82)
        
        if not mob_m.get("is_grouped", False):
            # Одиночный дроп (старая ветка на всякий случай)
            count_str = f" [{mob_m['drop'].get('min', 1)}]"
            left_text = f"- {mob_m['drop']['name']}{count_str}"
            right_text = f"{mob_m['drop']['chance']*100:.4f}%"
            
            screen.blit(self.core.font_small.render(left_text, True, cfg.TEXT_COLOR), (int(w * 0.14), dy))
            t_percent = self.core.font_small.render(right_text, True, cfg.TEXT_COLOR)
            screen.blit(t_percent, (right_align_x - t_percent.get_width(), dy))
        else:
            for group in mob_m["groups"]:
                # Рендерим заголовок группы и его общий процент
                g_left = f"Group Drop Chance:"
                g_right = f"{group['group_chance']*100:.3f}%"
                
                screen.blit(self.core.font_small.render(g_left, True, cfg.DROP_COLOR), (int(w * 0.14), dy))
                t_g_percent = self.core.font_small.render(g_right, True, cfg.DROP_COLOR)
                screen.blit(t_g_percent, (right_align_x - t_g_percent.get_width(), dy))
                
                dy += step_y
                
                # Рендерим предметы внутри этой группы
                for item in group["items"]:
                    item_name_str = str(item['name'])
                    
                    # Делаем имя красивым, заменяя нижние подчеркивания на пробелы
                    clean_name = item_name_str.replace("_", " ").title()
                    # Если название всё равно слишком длинное, аккуратно режем его
                    name = clean_name[:16] + ".." if len(clean_name) > 18 else clean_name
                    
                    # Количество: [1] или [22-40]
                    imin = item.get("min", 1)
                    imax = item.get("max", 1)
                    count_text = f" [{imin}]" if imin == imax else f" [{imin}-{imax}]"
                    
                    # Левая часть строки (Название + количество)
                    left_line = f"  * {name}{count_text}"
                    # Правая часть строки (Шанс внутри группы)
                    right_line = f"{item['chance_in_group']*100:.0f}%"
                    
                    # Отрисовка левой части
                    screen.blit(self.core.font_small.render(left_line, True, cfg.TEXT_COLOR), (int(w * 0.14), dy))
                    
                    # Отрисовка правой части (Выравнивание строго по правому краю невидимого столбца!)
                    t_item_percent = self.core.font_small.render(right_line, True, cfg.TEXT_COLOR)
                    screen.blit(t_item_percent, (right_align_x - t_item_percent.get_width(), dy))
                    
                    dy += step_y
                dy += int(step_y * 0.3)
