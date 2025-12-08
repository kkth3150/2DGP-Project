from GameObject import GameObject
from Resource_Manager import ResourceManager
from pico2d import *
from enum import Enum, auto
from Object_Manager import ObjectManager, OBJ

class UI_INDEX(Enum):
    INFO_BAR = auto()
    EXP_BAR = auto()
    HP_BAR = auto()
    MP_BAR = auto()
    BOSS_HP_BAR = auto()
    WIN = auto()  # 추가
    LOSE = auto()

class Default_UI(GameObject):
    def __init__(self, ui_type, player=None, x=400, y=50):
        width, height, img_key = 200, 20, None
        self.win_state = True  # Win(True) / Lose(False) 기본값

        if ui_type == UI_INDEX.HP_BAR:
            width, height = 146, 13
            img_key = "Hp_Bar"
        elif ui_type == UI_INDEX.MP_BAR:
            pass
        elif ui_type == UI_INDEX.EXP_BAR:
            width, height = 800, 80
            img_key = "UI_EXP_BAR"
        elif ui_type == UI_INDEX.BOSS_HP_BAR:
            width, height = 800, 15
            img_key = "Hp_Bar"
            self.boss = self.find_boss()
        elif ui_type == UI_INDEX.INFO_BAR:
            pass
        elif ui_type == UI_INDEX.WIN:
            width, height = 0, 0  # 크기는 이미지 그대로
            img_key = "Win"
        elif ui_type == UI_INDEX.LOSE:
            width, height = 0, 0  # 크기는 이미지 그대로
            img_key = "Lose"

        super().__init__(x, y, size=max(width, height))
        self.ui_type = ui_type
        self.player = player
        self.width = width
        self.height = height
        self.current_value = width
        self.full_width = width

        rm = ResourceManager.instance()
        if img_key:
            self.image = rm.get(img_key)
            if self.image:
                self.img_w = self.image.w
                self.img_h = self.image.h
        else:
            self.image = None
            self.img_w = 0
            self.img_h = 0

    def find_player(self):
        players = ObjectManager.instance().get_objects(OBJ.PLAYER)
        return players[0] if players else None

    def find_boss(self):
        boss = ObjectManager.instance().get_objects(OBJ.BOSS)
        return boss[0] if boss else None

    def update(self, dt):
        if self.ui_type == UI_INDEX.HP_BAR and self.player:
            if self.player.max_hp > 0:
                health_ratio = self.player.hp / self.player.max_hp
                self.width = int(self.full_width * health_ratio)
                self.width = max(0, self.width)
        elif self.ui_type == UI_INDEX.BOSS_HP_BAR and hasattr(self, 'boss') and self.boss:
            if self.boss.max_hp > 0:
                health_ratio = self.boss.hp / self.boss.max_hp
                self.width = int(self.full_width * health_ratio)
                self.width = max(0, self.width)
        # WIN_LOSE는 상태에 따라 이미지 표시하므로 update 필요 없음

    def render(self):
        if self.image:
            if self.ui_type == UI_INDEX.HP_BAR:
                draw_x = self.x - (self.full_width - self.width) / 2
                self.image.draw(draw_x, self.y, self.width, self.height)
            elif self.ui_type == UI_INDEX.BOSS_HP_BAR:
                draw_x = self.x - self.full_width / 2 + self.width / 2
                self.image.draw(draw_x, self.y, self.width, self.height)

            elif self.ui_type in (UI_INDEX.WIN, UI_INDEX.LOSE):
                if self.image:
                    canvas_w, canvas_h = get_canvas_width(), get_canvas_height()
                    self.image.draw(canvas_w // 2, canvas_h // 2)

            else:
                self.image.draw(self.x, self.y)

        # ---------------- WIN / LOSE 표시 ----------------
