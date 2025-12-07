from pico2d import *
from GameObject import GameObject
from Scroll_Manager import ScrollManager
from Resource_Manager import ResourceManager
from Object_Manager import OBJ
import random


class DropItem(GameObject):
    def __init__(self, x, target_y, item_id=0):
        super().__init__(x, target_y + 10, size=30)

        rm = ResourceManager.instance()
        self.image = rm.get("Potion")

        self.start_y = self.y
        self.target_y = target_y

        self.vy = 500       # 처음 위로 튀기기
        self.gravity = 1300

        self.rotation = 360
        self.rot_speed = 1000

        self.life_time = 6  # 바닥 도착 후 유지 시간
        self.landed = False

    def update(self, dt):

        if not self.landed:
            self.vy -= self.gravity * dt
            self.y += self.vy * dt

            # 공중에서만 회전
            self.rotation += self.rot_speed * dt

            if self.y <= self.target_y:
                self.y = self.target_y
                self.vy = 0
                self.rot_speed = 0
                self.rotation = 0  # ← 착지하면 **정자세로 초기화**
                self.landed = True

        else:
            self.life_time -= dt
            if self.life_time <= 0:
                return 1

        if self.is_dead:
            return 1

        return 0

    def render(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()

        self.image.rotate_draw(
            math.radians(self.rotation),
            self.x - scroll_x,
            self.y - scroll_y,
            32, 32
        )

        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        x1, y1, x2, y2 = self.get_col_rect()
        draw_rectangle(x1 - scroll_x, y1 - scroll_y, x2 - scroll_x, y2 - scroll_y)

    def get_col_rect(self):
        size = 20
        return (self.x - size, self.y - size, self.x + size, self.y + size)

