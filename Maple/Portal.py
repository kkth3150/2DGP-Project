from GameObject import GameObject
from Resource_Manager import ResourceManager
from Animation_Manager import Animation
from Scroll_Manager import ScrollManager
from pico2d import *

class Portal(GameObject):
    def __init__(self, x, y, target_level):
        super().__init__(x, y, size=80)

        self.target_level = target_level

        rm = ResourceManager.instance()
        self.image = rm.get("Portal")  # 129x178 스프라이트 이미지

        self.anim = Animation(
            self.image,
            129,        # frame_width
            178,        # frame_height
            {'x':0,'y':0,'frame_count':6},
            fps=6,
            loop=True
        )

    def update(self, dt):
        self.anim.update(dt)

    def render(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        self.anim.draw(self.x, self.y, scroll_x, scroll_y)

    def get_col_rect(self):
        return (self.x - 40, self.y - 60, self.x + 40, self.y + 60)

    def render_hitbox(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        x1, y1, x2, y2 = self.get_col_rect()
        draw_rectangle(x1 - scroll_x, y1 - scroll_y, x2 - scroll_x, y2 - scroll_y)