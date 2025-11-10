from GameObject import GameObject
from Input_Manager import Input_manager
from Scroll_Manager import ScrollManager
from Line_Manager import LineManager
from pico2d import *

class Player(GameObject):
    def __init__(self, x=400, y=300):  # 초기 위치
        super().__init__(x, y, size=50)
        self.hp = 100
        self.speed = 200          # 이동 속도
        self.vy = 0               # Y 속도
        self.gravity = -1000      # 중력 (픽셀/s²)
        self.jump_power = 500     # 점프 힘
        self.on_ground = False    # 라인 위인지

        # 스크롤 초기화
        scroll_mgr = ScrollManager.instance()
        scroll_mgr.scroll_x = 0
        scroll_mgr.scroll_y = 0

    def update(self, dt):
        if self.is_dead:
            return

        self.handle_input(dt)      # 키 입력 처리
        self.apply_gravity(dt)     # 중력 적용 및 라인 충돌 체크
        self.update_scroll()       # 스크롤 업데이트

    def handle_input(self, dt):
        # 좌우 이동
        dx = 0
        if Input_manager.instance().Key_Pressing(SDLK_a):
            dx = -self.speed * dt
        if Input_manager.instance().Key_Pressing(SDLK_d):
            dx = self.speed * dt

        self.x += dx

        # 점프
        if Input_manager.instance().Key_Down(SDLK_SPACE) and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False

    def apply_gravity(self, dt):
        # Y 속도에 중력 적용
        self.vy += self.gravity * dt
        self.y += self.vy * dt

        # 바닥 기준 충돌 체크
        foot_y = self.y - self.size / 2  # 플레이어 바닥 위치
        collided_y, collision = LineManager.instance().collision_line(self.x, foot_y, move_y=abs(self.vy * dt))

        if collision and self.vy <= 0:  # 떨어질 때만 바닥에 붙도록
            self.y = collided_y + self.size / 2
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def update_scroll(self):
        scroll_mgr = ScrollManager.instance()
        left_border = 300
        right_border = 500
        top_border = 150
        bottom_border = 200

        if self.x - scroll_mgr.scroll_x < left_border:
            scroll_mgr.set_scroll_x(self.x - scroll_mgr.scroll_x - left_border)
        elif self.x - scroll_mgr.scroll_x > right_border:
            scroll_mgr.set_scroll_x(self.x - scroll_mgr.scroll_x - right_border)

        if self.y - scroll_mgr.scroll_y < top_border:
            scroll_mgr.set_scroll_y(self.y - scroll_mgr.scroll_y - top_border)
        elif self.y - scroll_mgr.scroll_y > bottom_border:
            scroll_mgr.set_scroll_y(self.y - scroll_mgr.scroll_y - bottom_border)

    def render(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        draw_x = self.x - scroll_x
        draw_y = self.y - scroll_y

        draw_rectangle(draw_x - self.size / 2, draw_y - self.size / 2,
                       draw_x + self.size / 2, draw_y + self.size / 2)

    def late_update(self):
        pass

    def release(self):
        pass