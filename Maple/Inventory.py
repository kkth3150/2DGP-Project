from GameObject import GameObject
from pico2d import *
from Resource_Manager import ResourceManager

class Inventory(GameObject):
    def __init__(self, player, x=400, y=300):
        super().__init__(x, y)

        self.player = player

        rm = ResourceManager.instance()
        self.image = rm.get("Inventory")
        self.potion_img = rm.get("Potion")

        self.potion_count = 0

        self.is_open = False

        # 슬롯 위치 (UI 기준 – 고정 좌표)
        self.slot_x = self.x -70
        self.slot_y = self.y +115
        self.slot_size = 32

    def add_potion(self, count=1):
        self.potion_count += count

    def use_potion(self):
        if self.potion_count > 0:
            self.potion_count -= 1
            return True  # 사용 성공
        return False     # 사용 불가

    def update(self, dt):
        pass

    def render(self):
        if not self.is_open:
            return

        self.image.draw(self.x, self.y)

        slot_draw_x = self.slot_x
        slot_draw_y = self.slot_y

        if self.potion_count > 0:
            self.potion_img.draw(slot_draw_x, slot_draw_y, 32, 32)

