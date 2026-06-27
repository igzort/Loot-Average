# config.py
from mobs.wolf import WOLF_DATA
from mobs.werewolf import WEREWOLF_DATA
from mobs.orc_grunt import ORC_GRUNT_DATA

WIDTH = 450
HEIGHT = 800
FPS = 60

# Цвета (RGB)
BACKGROUND = (30, 30, 35)
UI_PANEL = (45, 45, 50)
UI_BORDER = (70, 70, 75)
ACTIVE_TAB = (100, 80, 60)
INACTIVE_TAB = (50, 50, 55)
TEXT_COLOR = (240, 240, 240)
DROP_COLOR = (255, 215, 0)
EMPTY_COLOR = (120, 120, 120)
RESET_COLOR = (160, 50, 50)
MODAL_BG = (20, 20, 25)
BTN_DROP = (70, 60, 100)

# Глобальная база данных мобов, собранная из папки mobs/
MOBS_DATA = {
    "Wolf": WOLF_DATA,
    "Werewolf": WEREWOLF_DATA,
    "Orc Grunt": ORC_GRUNT_DATA
}
