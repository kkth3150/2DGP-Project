from GameObject import GameObject
from Input_Manager import Input_manager
from Scroll_Manager import ScrollManager
from Line_Manager import LineManager
from pico2d import *
from enum import Enum, auto
from Resource_Manager import ResourceManager
from Animation_Manager import Animation
from Inventory import Inventory
from Skill import Skill,Skill_Kind
from Object_Manager import ObjectManager, OBJ

class PlayerState(Enum):
    IDLE = auto()
    WALK = auto()
    ATTACK = auto()
    JUMP = auto()


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()


class Player(GameObject):
    def __init__(self, x=400, y=300):
        super().__init__(x, y, size=50)

        self.inventory = Inventory(self, x=400, y=300)
        self.hp = 100
        self.speed = 200
        self.vy = 0
        self.gravity = 1300
        self.jump_power = 500
        self.on_ground = False

        self.state = PlayerState.IDLE
        self.direction = Direction.RIGHT

        # 공격 타이머
        self.attack_timer = 0
        self.prev_state = PlayerState.IDLE

        self.combo_step = 0          # 현재 콤보 단계
        self.combo_timer = 0         # 콤보 유지 시간
        self.combo_timeout = 0.7     # 0.7초 안에 눌러야 다음 공격


        rm = ResourceManager.instance()
        self.image_left = rm.get("Player_Left")
        self.image_right = rm.get("Player_Right")

        self.animations = {
            (PlayerState.IDLE, Direction.RIGHT): Animation(self.image_right, 128, 128,
                                                           {'x': 0, 'y': 512, 'frame_count': 4}),
            (PlayerState.WALK, Direction.RIGHT): Animation(self.image_right, 128, 128,
                                                           {'x': 0, 'y': 384, 'frame_count': 4}),
            (PlayerState.ATTACK, Direction.RIGHT): Animation(self.image_right, 128, 128,
                                                             {'x': 0, 'y': 256, 'frame_count': 3}),
            (PlayerState.JUMP, Direction.RIGHT): Animation(self.image_right, 128, 128,
                                                           {'x': 384, 'y': 256, 'frame_count': 1}),

            (PlayerState.IDLE, Direction.LEFT): Animation(self.image_left, 128, 128,
                                                          {'x': 0, 'y': 512, 'frame_count': 4}),
            (PlayerState.WALK, Direction.LEFT): Animation(self.image_left, 128, 128,
                                                          {'x': 0, 'y': 384, 'frame_count': 4}),
            (PlayerState.ATTACK, Direction.LEFT): Animation(self.image_left, 128, 128,
                                                            {'x': 0, 'y': 256, 'frame_count': 3}),
            (PlayerState.JUMP, Direction.LEFT): Animation(self.image_left, 128, 128,
                                                          {'x': 384, 'y': 256, 'frame_count': 1}),
        }

        scroll_mgr = ScrollManager.instance()
        scroll_mgr.scroll_x = 0
        scroll_mgr.scroll_y = 0

    def update(self, dt):
        if self.is_dead:
            return

        self.handle_attack_timer(dt)
        self.handle_input(dt)
        self.apply_gravity(dt)
        self.update_scroll()
        self.animations[(self.state, self.direction)].update(dt)
        self.inventory.update(dt)

    def handle_attack_timer(self, dt):
        if self.attack_timer > 0:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.attack_timer = 0
                self.state = self.prev_state  # 공격 끝나면 이전 상태로

        if self.combo_timer > 0:
            self.combo_timer -= dt
        else:
            self.combo_step = 0  # 시간 초과 시 콤보 초기화

    def handle_input(self, dt):
        dx = 0
        im = Input_manager.instance()

        # 지상 공격 중에는 이동 불가
        if self.state == PlayerState.ATTACK and self.on_ground:
            dx = 0
        else:
            if im.Key_Pressing(SDLK_LEFT):
                dx = -self.speed * dt
                self.direction = Direction.LEFT
                if self.on_ground and self.attack_timer == 0:
                    self.state = PlayerState.WALK
            elif im.Key_Pressing(SDLK_RIGHT):
                dx = self.speed * dt
                self.direction = Direction.RIGHT
                if self.on_ground and self.attack_timer == 0:
                    self.state = PlayerState.WALK
            else:
                if self.on_ground and self.attack_timer == 0:
                    self.state = PlayerState.IDLE

        # 점프
        if im.Key_Down(SDLK_LALT) and self.on_ground and self.attack_timer == 0:
            self.vy = self.jump_power
            self.on_ground = False
            self.state = PlayerState.JUMP
        # 공격
        if im.Key_Down(SDLK_LCTRL) and self.attack_timer == 0:
            self.prev_state = self.state
            self.state = PlayerState.ATTACK
            self.attack_timer = 0.45

            self.combo_step += 1
            if self.combo_step > 7:
                self.combo_step = 1

            self.combo_timer = self.combo_timeout

            skill_kind = self.get_combo_skill(self.combo_step, self.direction)
            skill = Skill(self.x, self.y, skill_kind)
            ObjectManager.instance().add_object(skill, OBJ.EFFECT)

        if im.Key_Down(SDLK_i):
            self.inventory.is_open = not self.inventory.is_open

        self.x += dx

    def apply_gravity(self, dt):
        self.vy -= self.gravity * dt
        new_y = self.y + self.vy * dt

        foot_y = new_y - self.size / 2
        collided_y, collided = LineManager.instance().collision_line(self.x, foot_y, abs(self.vy * dt))

        if collided and self.vy <= 0:
            self.y = collided_y + self.size / 2
            self.vy = 0
            self.on_ground = True
        else:
            self.y = new_y
            self.on_ground = False

    def update_scroll(self):
        scroll_mgr = ScrollManager.instance()
        left_border, right_border = 300, 500
        top_border, bottom_border = 150, 200

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
        anim = self.animations[(self.state, self.direction)]
        anim.draw(self.x, self.y, scroll_x, scroll_y)

        self.inventory.render()

    def late_update(self):
        pass

    def release(self):
        pass

    def get_combo_skill(self, step, direction):
        mapping = {
            1: (Skill_Kind.Swing1_L, Skill_Kind.Swing1_R),
            2: (Skill_Kind.Swing2_L, Skill_Kind.Swing2_R),
            3: (Skill_Kind.Swing3_L, Skill_Kind.Swing3_R),
            4: (Skill_Kind.Beyond1_L, Skill_Kind.Beyond1_R),
            5: (Skill_Kind.Beyond2_L, Skill_Kind.Beyond2_R),
            6: (Skill_Kind.Beyond3_L, Skill_Kind.Beyond3_R),
            7: (Skill_Kind.Beyond4_L, Skill_Kind.Beyond4_R),
        }
        left_skill, right_skill = mapping.get(step, (Skill_Kind.Swing1_L, Skill_Kind.Swing1_R))
        return left_skill if direction == Direction.LEFT else right_skill