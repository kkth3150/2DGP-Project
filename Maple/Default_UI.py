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

class Default_UI(GameObject):
    def __init__(self, ui_type, player=None, x=400, y=50):
        width, height, img_key, img_path = 200, 20, None, None
        if ui_type == UI_INDEX.HP_BAR:
            width, height = 146, 13
            img_key = "Hp_Bar"  # ResourceManager에서 불러올 이미지 키
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

    def update(self, dt):
        if self.ui_type == UI_INDEX.HP_BAR and self.player:
            if self.player.max_hp > 0:
                health_ratio = self.player.hp / self.player.max_hp
                self.width = int(self.full_width * health_ratio)
                self.width = max(0, self.width)  # 너비는 최소 0

        elif self.ui_type == UI_INDEX.MP_BAR and self.player:
            pass  # 적용 안 함
        elif self.ui_type == UI_INDEX.EXP_BAR and self.player:
            pass  # 적용 안 함
        elif self.ui_type == UI_INDEX.INFO_BAR:
            pass  # 적용 안 함

    def render(self):
        if self.image:
            # 스크롤 매니저를 사용하지 않는 UI라고 가정하고 진행합니다.

            if self.ui_type == UI_INDEX.HP_BAR:
                # 🟢 HP Bar는 현재 너비(self.width)와 높이(self.height)를 사용해 그립니다.

                # 1. 화면에 그릴 중심 X 좌표 조정 (좌측 정렬을 위함)
                # 바의 너비가 줄어들 때, 왼쪽 끝이 고정되도록 중심 좌표를 왼쪽으로 이동시킵니다.
                draw_x = self.x - (self.full_width - self.width) / 2

                # self.image.draw(x, y, w, h)를 사용하여 크기를 조절합니다.
                # 참고: 이 방법은 HP가 줄어들 때 이미지가 찌그러져 보일 수 있습니다.
                self.image.draw(
                    draw_x,
                    self.y,
                    self.width,  # 현재 HP 비율에 맞춰 계산된 너비
                    self.height  # 원래 높이
                )
            else:
                # MP/EXP/INFO BAR 등 기타 UI는 이미지 전체를 그립니다.
                self.image.draw(self.x, self.y)