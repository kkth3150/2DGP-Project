from GameObject import GameObject
from pico2d import *
from Resource_Manager import ResourceManager
from Input_Manager import Input_manager

class Inventory(GameObject):
    def __init__(self, player, x=400, y=300):
        super().__init__(x, y)
        self.player = player
        self.is_open = False  # 처음에는 닫힘
        rm = ResourceManager.instance()
        self.image = rm.get("Inventory")  # 나중에 실제 이미지 넣으면 됨

    def toggle(self):
        self.is_open = not self.is_open

    def update(self, dt):
        pass

    def render(self):
        if self.is_open and self.image:
            self.image.draw(self.x, self.y)