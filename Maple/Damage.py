from GameObject import GameObject
from Resource_Manager import ResourceManager
from pico2d import *
import time
from Scroll_Manager import ScrollManager

class DamageNumber(GameObject):
    def __init__(self, x, y, value, critical = False):
        super().__init__(x, y, size=0)
        self.value = str(value)[-8:]  # 최대 8자리
        self.critical = critical
        self.start_time = time.time()
        self.duration = 0.5
        self.dy = 30
        self.offset_y = 0
        self.is_dead = False
        self.spacing = 25          # 글자 간격 (위치 기준)

        rm = ResourceManager.instance()
        # 숫자 이미지 로드
        self.num_images = [
            rm.get("Num_0"), rm.get("Num_1"), rm.get("Num_2"),
            rm.get("Num_3"), rm.get("Num_4"), rm.get("Num_5"),
            rm.get("Num_6"), rm.get("Num_7"), rm.get("Num_8"),
            rm.get("Num_9")
        ]
        self.critical_image = rm.get("Critical")

    def update(self, dt):
        elapsed = time.time() - self.start_time
        if elapsed > self.duration:
            self.is_dead = True
            return
        self.offset_y = (elapsed / self.duration) * self.dy

    def render(self):
        if self.is_dead:
            return

        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        start_x = self.x - scroll_x
        start_y = self.y + self.offset_y - scroll_y

        # 크리티컬 표시
        self.critical_image.draw(start_x, start_y)
        start_x += self.spacing  # 숫자 시작 위치는 항상 일정 간격

        for i, ch in enumerate(self.value):
            idx = int(ch)
            img = self.num_images[idx]
            img.draw(start_x + i * self.spacing, start_y)