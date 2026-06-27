# ui_inventory.py
import pygame
import config as cfg
import os
from items.items_py import ItemManager

from items.items_materials import ITEMS_MATERIALS
from items.items_recipes import ITEMS_RECIPES
from items.items_gear import ITEMS_GEAR
from items.items_misc import ITEMS_MISC

ALL_ITEMS = {}
ALL_ITEMS.update(ITEMS_MATERIALS)
ALL_ITEMS.update(ITEMS_RECIPES)
ALL_ITEMS.update(ITEMS_GEAR)
ALL_ITEMS.update(ITEMS_MISC)

class UIInventory:
    def __init__(self, core, textures):
        self.core = core
        w, h = cfg.WIDTH, cfg.HEIGHT
        
        # 1. ГЕОМЕТРИЯ КЛЕТОК (Идеальные квадраты)
        self.cell_size = int(w * 0.205)
        self.icon_size = self.cell_size - 6
        
        self.item_manager = ItemManager(self.icon_size)
        self.textures = textures
        self.textures.update(self.item_manager.textures)
        
        # Жестко восстанавливаем и фиксируем пиксельные картинки
        self._fix_asset_textures()
        
        # 2. РАБОЧАЯ ОБЛАСТЬ (Строго 4 колонки на 3 видимых ряда!)
        self.start_inv_x = int(w * 0.05)
        self.start_inv_y = int(h * 0.552)
        self.visible_rows = 3  # Срезали до 3 рядов, чтобы не лезло под MOBS MENU!
        self.total_cells = 40
        self.total_rows = self.total_cells // 4
        
        # 3. ПОЛОСА ПРОКРУТКИ (Укорочена ровно под 3 ряда ячеек)
        self.scrollbar_x = self.start_inv_x + 4 * self.cell_size + 4
        self.scrollbar_y = self.start_inv_y
        self.scrollbar_w = int(w * 0.05)
        self.scrollbar_h = self.visible_rows * self.cell_size - 6
        self.scrollbar_rect = pygame.Rect(self.scrollbar_x, self.scrollbar_y, self.scrollbar_w, self.scrollbar_h)
        
        self.scroll_row = 0
        self.is_dragging = False
        
        # 4. МИКРО-КНОПКА ЧИСТКИ "Х"
        self.btn_clean_mini = pygame.Rect(self.scrollbar_x, int(h * 0.505), self.scrollbar_w, int(h * 0.035))
        
        # Возвращаем кнопку выбора мобов на её законное фиксированное место
        self.core.btn_mobs_menu_rect = pygame.Rect(int(w * 0.05), int(h * 0.89), int(w * 0.90), int(h * 0.07))

    def _fix_asset_textures(self):
        """Загружает картинки строго из корня проекта, где лежит ui_inventory.py."""
        # Находим корень проекта (так как ui_inventory.py лежит прямо в корне)
        project_root = os.path.dirname(os.path.abspath(__file__))
        
        items_list = list(ALL_ITEMS.keys())
        for item_id in items_list:
            # Собираем путь: корень -> assets -> items -> файл.png
            if item_id.startswith("rec_"):
                path = os.path.join(project_root, "assets", "items", "recipes", f"{item_id}.png")
            else:
                path = os.path.join(project_root, "assets", "items", f"{item_id}.png")
                
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                # Сжатие в 16х16 для жесткого пиксель-арта Lineage 2
                small_img = pygame.transform.scale(img, (16, 16))
                # Растягивание на всю клетку инвентаря без сглаживания
                self.textures[item_id] = pygame.transform.scale(small_img, (self.icon_size, self.icon_size))
            else:
                # ЗАЩИТА: Если файла .png в ассетах нет, берём процедурную иконку,
                # которую сгенерировал ItemManager при старте, и растягиваем её на всю ячейку.
                if item_id in self.textures:
                    # Извлекаем уже готовую текстуру, чтобы ячейка не оставалась пустой
                    old_tex = self.textures[item_id]
                    self.textures[item_id] = pygame.transform.scale(old_tex, (self.icon_size, self.icon_size))



    def handle_scroll_click(self, mouse_pos):
        if self.scrollbar_rect.collidepoint(mouse_pos):
            self.is_dragging = True
            self._update_scroll_from_mouse(mouse_pos[1]) # Передаем только Y координату!

    def handle_scroll_drag(self, mouse_pos):
        if self.is_dragging:
            self._update_scroll_from_mouse(mouse_pos[1]) # Передаем только Y координату!

    def _update_scroll_from_mouse(self, mouse_y):
        relative_y = mouse_y - self.scrollbar_y
        percentage = max(0.0, min(1.0, relative_y / self.scrollbar_h))
        max_scrollable_rows = self.total_rows - self.visible_rows
        self.scroll_row = int(percentage * max_scrollable_rows)

    def draw(self, screen, logic):
        w, h = cfg.WIDTH, cfg.HEIGHT
        m_pos = pygame.mouse.get_pos()
        m_pressed = pygame.mouse.get_pressed()
        
        if not m_pressed[0]:
            self.is_dragging = False
        else:
            self.handle_scroll_drag(m_pos)

        # РЕНДЕР КНОПКИ "Х"
        pygame.draw.rect(screen, cfg.RESET_COLOR, self.btn_clean_mini, border_radius=4)
        pygame.draw.rect(screen, cfg.UI_BORDER, self.btn_clean_mini, 1, border_radius=4)
        t_clean = self.core.font_small.render("X", True, cfg.TEXT_COLOR)
        screen.blit(t_clean, (self.btn_clean_mini.centerx - t_clean.get_width()//2, self.btn_clean_mini.centery - t_clean.get_height()//2))

        screen.blit(self.core.font_big.render("INVENTORY", True, cfg.TEXT_COLOR), (self.start_inv_x, int(h * 0.505)))

        all_items_in_inv = list(logic.inventory.keys())

        # РЕНДЕР СЕТКИ 4х3 (12 ячеек на экране)
        for row in range(self.visible_rows):
            actual_row = row + self.scroll_row
            for col in range(4):
                cx = self.start_inv_x + col * self.cell_size
                cy = self.start_inv_y + row * self.cell_size
                cell_rect = pygame.Rect(cx, cy, self.cell_size - 6, self.cell_size - 6)
                
                pygame.draw.rect(screen, (25, 25, 30), cell_rect, border_radius=4)
                pygame.draw.rect(screen, cfg.UI_BORDER, cell_rect, 1, border_radius=4)
                
                item_index = actual_row * 4 + col
                if item_index < len(all_items_in_inv):
                    item_id = all_items_in_inv[item_index]
                    real_count = logic.inventory[item_id]
                    
                    if item_id in self.textures:
                        icon_x = cx + (cell_rect.width - self.textures[item_id].get_width()) // 2
                        icon_y = cy + (cell_rect.height - self.textures[item_id].get_height()) // 2
                        screen.blit(self.textures[item_id], (icon_x, icon_y))

                    display_count = self.item_manager.format_adena_count(item_id, real_count)
                    count_txt = self.core.font_small.render(display_count, True, cfg.TEXT_COLOR)
                    
                    count_bg = pygame.Rect(cx + cell_rect.width - count_txt.get_width() - 8, cy + cell_rect.height - count_txt.get_height() - 5, count_txt.get_width() + 4, count_txt.get_height() + 2)
                    pygame.draw.rect(screen, (15, 15, 20, 180), count_bg, border_radius=2)
                    screen.blit(count_txt, (cx + cell_rect.width - count_txt.get_width() - 6, cy + cell_rect.height - count_txt.get_height() - 4))

        # РЕНДЕР СКРОЛЛБАРА
        pygame.draw.rect(screen, (20, 20, 25), self.scrollbar_rect, border_radius=4)
        pygame.draw.rect(screen, cfg.UI_BORDER, self.scrollbar_rect, 1, border_radius=4)
        
        max_scrollable_rows = self.total_rows - self.visible_rows
        slider_h = self.scrollbar_h // (max_scrollable_rows + 1)
        slider_y = self.scrollbar_y + (self.scroll_row * (self.scrollbar_h - slider_h) // max_scrollable_rows if max_scrollable_rows > 0 else 0)
        slider_rect = pygame.Rect(self.scrollbar_x + 2, slider_y, self.scrollbar_w - 4, slider_h)
        
        pygame.draw.rect(screen, cfg.ACTIVE_TAB, slider_rect, border_radius=4)

        # ТУЛТИПЫ ПРИ ЗАЖАТИИ
        if m_pressed[0] and not self.is_dragging:
            for r in range(self.visible_rows):
                for c in range(4):
                    icx = self.start_inv_x + c * self.cell_size
                    icy = self.start_inv_y + r * self.cell_size
                    if pygame.Rect(icx, icy, self.cell_size - 6, self.cell_size - 6).collidepoint(m_pos):
                        actual_r = r + self.scroll_row
                        idx = actual_r * 4 + c
                        if idx < len(all_items_in_inv):
                            item_id = all_items_in_inv[idx]
                            total = logic.inventory[item_id]
                            item_data = ALL_ITEMS.get(item_id)
                            display_name = item_data["name"] if item_data else item_id.replace("_", " ").title()
                            
                            full_info = f"{display_name} ({total})"
                            tip_text = self.core.font_small.render(full_info, True, cfg.DROP_COLOR)
                            tip_bg = pygame.Rect(m_pos[0] - 80, m_pos[1] - 35, tip_text.get_width() + 16, 25)
                            pygame.draw.rect(screen, (10, 10, 15), tip_bg, border_radius=4)
                            pygame.draw.rect(screen, cfg.DROP_COLOR, tip_bg, 1, border_radius=4)
                            screen.blit(tip_text, (tip_bg.x + 8, tip_bg.y + 5))
