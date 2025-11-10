from GameObject import GameObject
from Resource_Manager import ResourceManager
from pico2d import *
from enum import Enum, auto

class UI_INDEX(Enum):
    INFO_BAR = auto()
    EXP_BAR = auto()
    HP_BAR = auto()
    MP_BAR = auto()

class Default_UI(GameObject):
    def __init__(self, ui_type, player=None, x=0, y=0):
        width, height, img_key, img_path = 200, 20, None, None
        if ui_type == UI_INDEX.HP_BAR:
            pass
        elif ui_type == UI_INDEX.MP_BAR:
            pass
        elif ui_type == UI_INDEX.EXP_BAR:
            width, height = 800, 80
            img_key = "UI_EXP_BAR"
        elif ui_type == UI_INDEX.INFO_BAR:
            pass

        super().__init__(x, y, size=max(width, height))
        self.ui_type = ui_type
        self.player = player
        self.width = width
        self.height = height
        self.current_value = width

        rm = ResourceManager.instance()
        if img_key:
            self.image = rm.get(img_key)
        else:
            self.image = None



    def update(self, dt):
        if self.ui_type == UI_INDEX.HP_BAR and self.player:
            pass
        elif self.ui_type == UI_INDEX.MP_BAR and self.player:
            pass
        elif self.ui_type == UI_INDEX.EXP_BAR and self.player:
            pass
        elif self.ui_type == UI_INDEX.INFO_BAR:
            pass

    def render(self):
        if self.image:
            self.image.draw(self.x, self.y)  # x, y는 중심 좌표