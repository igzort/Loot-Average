# logic.py
import pygame
import random
from config import MOBS_DATA

# Импортируем словари из подпапки items/
from items.items_materials import ITEMS_MATERIALS
from items.items_recipes import ITEMS_RECIPES
from items.items_gear import ITEMS_GEAR
from items.items_misc import ITEMS_MISC

# Объединяем их в единую базу данных предметов
ALL_ITEMS = {}
ALL_ITEMS.update(ITEMS_MATERIALS)
ALL_ITEMS.update(ITEMS_RECIPES)
ALL_ITEMS.update(ITEMS_GEAR)
ALL_ITEMS.update(ITEMS_MISC)

class GameLogic:
    def __init__(self):
        self.current_mob_type = "Wolf"
        self.kills = {"Wolf": 0, "Werewolf": 0, "Orc Grunt": 0}
        self.inventory = {}
        self.drop_log = []
        
        # Окна интерфейса
        self.show_mobs_menu = False
        self.show_droplist_for = None
        
        # Макросы
        self.macro_mode = 0  
        self.last_macro_time = pygame.time.get_ticks()
        
        # Текущая вкладка инвентаря
        self.current_tab = 0
        
        # Настройка времени на убийство моба
        self.time_per_kill = 5

    def toggle_time_per_kill(self):
        """Переключает время на убийство моба между 5, 10 и 15 секундами."""
        if self.time_per_kill == 5:
            self.time_per_kill = 10
        elif self.time_per_kill == 10:
            self.time_per_kill = 15
        else:
            self.time_per_kill = 5
        self.drop_log.append(f"Kill Time: {self.time_per_kill}s")
        self._trim_log()

    def change_mob(self, mob_type):
        if mob_type in MOBS_DATA and self.current_mob_type != mob_type:
            self.current_mob_type = mob_type
            self.drop_log.append(f"Target: {mob_type}")
            self.show_mobs_menu = False
            self._trim_log()

    def clean_inventory(self):
        self.inventory.clear()
        self.drop_log.append("Inventory Cleaned!")
        self._trim_log()

    def toggle_macro(self, mode_id):
        if self.macro_mode == mode_id:
            self.macro_mode = 0
            self.drop_log.append("Macro: OFF")
        else:
            self.macro_mode = mode_id
            intervals = {1: "0.5s", 2: "1.0s", 3: "0.2s"}
            self.drop_log.append(f"Macro: Loop {intervals[mode_id]}")
        self.last_macro_time = pygame.time.get_ticks()
        self._trim_log()

    def update_macros(self):
        if self.macro_mode == 0:
            return
        current_time = pygame.time.get_ticks()
        intervals = {1: 500, 2: 1000, 3: 200}
        interval = intervals[self.macro_mode]

        if current_time - self.last_macro_time >= interval:
            self.hit_mob()
            self.last_macro_time = current_time

    def calculate_l2_drop(self):
        dropped = []
        mob_info = MOBS_DATA[self.current_mob_type]
        
        if not mob_info.get("is_grouped", False):
            drop_info = mob_info["drop"]
            if random.randint(1, 1000000) <= int(drop_info["chance"] * 1000000):
                dropped.append(drop_info["name"])
            return dropped

        for group in mob_info["groups"]:
            if random.randint(1, 1000000) <= int(group["group_chance"] * 1000000):
                items = group["items"]
                roll = random.random()
                cumulative_chance = 0.0
                for item in items:
                    cumulative_chance += item["chance_in_group"]
                    if roll <= cumulative_chance:
                        dropped.append(item["name"])
                        break
        return dropped

    def _trim_log(self):
        while len(self.drop_log) > 4:
            self.drop_log.pop(0)

    def hit_mob(self):
        self.kills[self.current_mob_type] += 1
        loot = self.calculate_l2_drop()
        mob_info = MOBS_DATA[self.current_mob_type]
        
        if loot:
            for item_id in loot:
                item_data = ALL_ITEMS.get(item_id)
                display_name = item_data["name"] if item_data else item_id.replace("_", " ").title()

                # Ищем min/max количества в настройках дроп-листа моба
                count_to_add = 1
                if mob_info.get("is_grouped", False):
                    for group in mob_info["groups"]:
                        for item in group["items"]:
                            if item["name"] == item_id:
                                imin = item.get("min", 1)
                                imax = item.get("max", 1)
                                count_to_add = random.randint(imin, imax)
                                break
                else:
                    if mob_info["drop"]["name"] == item_id:
                        imin = mob_info["drop"].get("min", 1)
                        imax = mob_info["drop"].get("max", 1)
                        count_to_add = random.randint(imin, imax)

                # Выводим в лог информацию о количестве
                if count_to_add > 1:
                    self.drop_log.append(f"Dropped: {display_name} ({count_to_add})!")
                else:
                    self.drop_log.append(f"Dropped: {display_name}!")
                
                self.inventory[item_id] = self.inventory.get(item_id, 0) + count_to_add
        else:
            self.drop_log.append("No drop")

        self._trim_log()
