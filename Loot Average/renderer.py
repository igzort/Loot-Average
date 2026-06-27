# renderer.py
import pygame
import config as cfg
import os
from sprites import SpriteGenerator
from ui_core import UICore
from ui_inventory import UIInventory
from ui_menus import UIMenus

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.ui = UICore()
        self.textures = SpriteGenerator().all_textures
        
        if "Orc Grunt" not in self.textures:
            dummy_orc = pygame.Surface((128, 128))
            dummy_orc.fill((50, 120, 50))
            self.textures["Orc Grunt"] = pygame.transform.scale(dummy_orc, self.textures["Wolf"].get_size())

        self.inv_renderer = UIInventory(self.ui, self.textures)
        self.menu_renderer = UIMenus(self.ui)
        
        self.mob_img_rect = self.ui.mob_img_rect
        self.btn_macro1_rect = self.ui.btn_macro1_rect
        self.btn_macro2_rect = self.ui.btn_macro2_rect
        self.btn_macro3_rect = self.ui.btn_macro3_rect
        self.btn_clean_rect = self.ui.btn_clean_rect
        self.btn_mobs_menu_rect = self.ui.btn_mobs_menu_rect
        self.btn_close_mobs = self.ui.btn_close_mobs
        
        self.row_wolf_rect = self.ui.row_wolf_rect
        self.drop_wolf_rect = self.ui.drop_wolf_rect
        self.row_ww_rect = self.ui.row_ww_rect
        self.drop_ww_rect = self.ui.drop_ww_rect
        
        w, h = cfg.WIDTH, cfg.HEIGHT
        step_y = self.row_ww_rect.y - self.row_wolf_rect.y
        self.row_orc_rect = self.row_ww_rect.move(0, step_y)
        self.drop_orc_rect = self.drop_ww_rect.move(0, step_y)
        
        self.btn_close_drop = self.ui.btn_close_drop

        # НОВОЕ: Хитбокс для салатовой кнопки переключения времени (справа вверху)
        self.btn_change_time_rect = pygame.Rect(int(w * 0.80), int(h * 0.045), int(w * 0.15), int(h * 0.04))

    def _format_grind_time(self, total_seconds):
        if total_seconds == 0:
            return "0s"
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        time_parts = []
        if hours > 0: time_parts.append(f"{hours}h")
        if minutes > 0: time_parts.append(f"{minutes}m")
        if seconds > 0 or not time_parts: time_parts.append(f"{seconds}s")
        return " ".join(time_parts)

    def draw(self, logic):
        w, h = cfg.WIDTH, cfg.HEIGHT
        self.screen.fill(cfg.BACKGROUND)
        
        self.btn_mobs_menu_rect = self.ui.btn_mobs_menu_rect

        # 1. СТАТИСТИКА И МОБ
        current_kills = logic.kills[logic.current_mob_type]
        
        # Динамический расчёт времени на основе выбранного режима (5, 10 или 15 сек)
        total_seconds = current_kills * logic.time_per_kill
        time_string = self._format_grind_time(total_seconds)
        
        # Разводим строки: ставим КИЛЛЫ и ВРЕМЯ друг под другом слева!
        text_kills = self.ui.font_big.render(f"Kills ({logic.current_mob_type}): {current_kills}", True, cfg.TEXT_COLOR)
        self.screen.blit(text_kills, (int(w * 0.05), int(h * 0.015)))
        
        text_time = self.ui.font_big.render(f"Time: {time_string}", True, cfg.DROP_COLOR)
        self.screen.blit(text_time, (int(w * 0.05), int(h * 0.045)))

        # РЕНДЕР САЛАТОВОЙ КНОПКИ (НАПРОТИВ СТРОКИ TIME)
        salat_color = (124, 252, 0)
        pygame.draw.rect(self.screen, (35, 60, 20), self.btn_change_time_rect, border_radius=4)
        pygame.draw.rect(self.screen, salat_color, self.btn_change_time_rect, 1, border_radius=4)
        
        txt_btn = self.ui.font_small.render(f"{logic.time_per_kill}s", True, salat_color)
        self.screen.blit(txt_btn, (self.btn_change_time_rect.centerx - txt_btn.get_width()//2, self.btn_change_time_rect.centery - txt_btn.get_height()//2))


        # Смещаем имя моба чуть пониже, чтобы шапка не наезжала
        mob_lvl = cfg.MOBS_DATA[logic.current_mob_type]["level"]
        name_txt = self.ui.font_big.render(f"Lv.{mob_lvl} {logic.current_mob_type}", True, cfg.TEXT_COLOR)
        self.screen.blit(name_txt, (w // 2 - name_txt.get_width() // 2, int(h * 0.085)))
        
        # Моб тоже плавно уезжает чуть ниже
        self.ui.mob_img_rect.y = int(h * 0.12)
        self.mob_img_rect = self.ui.mob_img_rect
        self.screen.blit(self.textures[logic.current_mob_type], self.ui.mob_img_rect.topleft)

        # 2. СИСТЕМНЫЙ ЛОГ
        chat_rect = pygame.Rect(int(w * 0.05), int(h * 0.31), int(w * 0.90), int(h * 0.075))
        pygame.draw.rect(self.screen, (20, 20, 25), chat_rect, border_radius=6)
        pygame.draw.rect(self.screen, cfg.UI_BORDER, chat_rect, 1, border_radius=6)
        
        font_chat = pygame.font.SysFont("Courier", max(11, int(w * 0.034)), bold=True)
        step_y = int(h * 0.014) 
        visible_logs = list(reversed(logic.drop_log))[:4]
        
        for i, log in enumerate(visible_logs):
            color = cfg.DROP_COLOR if "Dropped" in log else cfg.TEXT_COLOR
            if "No drop" in log: color = cfg.EMPTY_COLOR
            display_log = log[:26] + ".." if len(log) > 28 else log
            self.screen.blit(font_chat.render(display_log, True, color), (int(w * 0.08), int(h * 0.314) + i * step_y))

        # 3. МАКРОСЫ
        macros_data = [(self.ui.btn_macro1_rect, "0.5s", 1), (self.ui.btn_macro2_rect, "1.0s", 2), (self.ui.btn_macro3_rect, "0.2s", 3)]
        for btn, text, mode in macros_data:
            b_color = cfg.ACTIVE_TAB if logic.macro_mode == mode else cfg.INACTIVE_TAB
            pygame.draw.rect(self.screen, b_color, btn, border_radius=5)
            pygame.draw.rect(self.screen, cfg.UI_BORDER, btn, 1, border_radius=5)
            t = self.ui.font_small.render(text, True, cfg.TEXT_COLOR)
            self.screen.blit(t, (btn.centerx - t.get_width()//2, btn.centery - t.get_height()//2))

        # 4. ИНВЕНТАРЬ
        self.inv_renderer.draw(self.screen, logic)

        # 5. КНОПКА МЕНЮ СНИЗУ
        pygame.draw.rect(self.screen, cfg.ACTIVE_TAB, self.ui.btn_mobs_menu_rect, border_radius=6)
        pygame.draw.rect(self.screen, cfg.UI_BORDER, self.ui.btn_mobs_menu_rect, 1, border_radius=6)
        t_mobs = self.ui.font_big.render("MOBS MENU", True, cfg.TEXT_COLOR)
        self.screen.blit(t_mobs, (self.ui.btn_mobs_menu_rect.centerx - t_mobs.get_width()//2, self.ui.btn_mobs_menu_rect.centery - t_mobs.get_height()//2))

        # 6. ВСПЛЫВАЮЩИЕ ОКНА
        if logic.show_mobs_menu:
            self.menu_renderer.draw_mobs(self.screen, logic)
        if logic.show_droplist_for is not None:
            self.menu_renderer.draw_drop(self.screen, logic)
