# items/items_py.py
import pygame
import config as cfg
import os

class ItemManager:
    def __init__(self, icon_size):
        self.icon_size = icon_size
        self.textures = self._generate_item_icons()

    def format_adena_count(self, item_name, count):
        """Ограничивает отображаемое число адены в ячейке до 999."""
        if item_name in ["adena", "Adena"] and count > 999:
            return "999"
        return str(count)

    def _generate_item_icons(self):
        sz = self.icon_size
        tex = {}
        
        # Список всех id предметов в игре
        items_list = [
            "adena", "coal", "varnish", "animal_bone", "animal_skin",
            "rec_leather_stockings", "rec_broad_sword",
            "short_bow", "iron_gloves", "leather_cap", "small_shield",
            "haste_potion", "lesser_hp_potion"
        ]
        
        for item_id in items_list:
            # Определяем путь к файлу (рецепты ищем в отдельной подпапке)
            if item_id.startswith("rec_"):
                path = os.path.join("assets", "items", "recipes", f"{item_id}.png")
            else:
                path = os.path.join("assets", "items", f"{item_id}.png")
            
            if os.path.exists(path):
                # 1. Загружаем реальную картинку
                img = pygame.image.load(path).convert_alpha()
                
                # 2. Сжимаем до 16х16 (создаем жесткий пиксельный эффект иконок L2)
                small_img = pygame.transform.scale(img, (16, 16))
                
                # 3. Растягиваем до размера ячейки инвентаря
                tex[item_id] = pygame.transform.scale(small_img, (sz, sz))
            else:
                # ЗАПАСНОЙ ВАРИАНТ (Если картинку еще не скачал)
                fallback = pygame.Surface((16, 16), pygame.SRCALPHA).convert_alpha()
                
                # Задаем цвета для временных квадратиков-заглушек по типам
                if item_id == "adena": color = (255, 215, 0)
                elif item_id.startswith("rec_"): color = (240, 230, 200) # свитки
                elif item_id in ["coal", "varnish", "animal_bone", "animal_skin"]: color = (130, 130, 130) # ресурсы
                elif item_id in ["haste_potion", "lesser_hp_potion"]: color = (220, 50, 50) # банки
                else: color = (70, 100, 180) # шмот / оружие
                
                fallback.fill(color)
                # Рисуем простую рамку на заглушке
                pygame.draw.rect(fallback, (30, 30, 30), (0, 0, 16, 16), 1)
                
                tex[item_id] = pygame.transform.scale(fallback, (sz, sz))
                
        return tex
