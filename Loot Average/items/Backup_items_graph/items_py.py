# items/items_py.py
import pygame
import config as cfg

# Импортируем модули графики из подпапки items_graph
from items.items_graph import graph_adena
from items.items_graph import graph_coal
from items.items_graph import graph_varnish
from items.items_graph import graph_bone
from items.items_graph import graph_skin
from items.items_graph import graph_recipe
from items.items_graph import graph_short_bow
from items.items_graph import graph_iron_gloves
from items.items_graph import graph_leather_cap
from items.items_graph import graph_small_shield
from items.items_graph import graph_haste_potion
from items.items_graph import graph_lesser_hp

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
        
        # 1. Материалы (Materials)
        tex["adena"] = graph_adena.get_texture(sz)
        tex["coal"] = graph_coal.get_texture(sz)
        tex["varnish"] = graph_varnish.get_texture(sz)
        tex["animal_bone"] = graph_bone.get_texture(sz)
        tex["animal_skin"] = graph_skin.get_texture(sz)

        # 2. Рецепты (Recipes) — используют один общий файл свитка
        tex["rec_leather_stockings"] = graph_recipe.get_texture(sz)
        tex["rec_broad_sword"] = graph_recipe.get_texture(sz)

        # 3. Экипировка (Gear)
        tex["short_bow"] = graph_short_bow.get_texture(sz)
        tex["iron_gloves"] = graph_iron_gloves.get_texture(sz)
        tex["leather_cap"] = graph_leather_cap.get_texture(sz)
        tex["small_shield"] = graph_small_shield.get_texture(sz)

        # 4. Расходники (Consumables)
        tex["haste_potion"] = graph_haste_potion.get_texture(sz)
        tex["lesser_hp_potion"] = graph_lesser_hp.get_texture(sz)

        return tex
