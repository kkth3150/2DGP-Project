from GameObject import GameObject
from enum import Enum, auto
from Resource_Manager import ResourceManager
from Animation_Manager import Animation
from Scroll_Manager import ScrollManager
from Object_Manager import ObjectManager, OBJ
from Line_Manager import LineManager
from pico2d import *

class SlimeState(Enum):
    IDLE = auto()
    MOVE = auto()
    HIT = auto()
    DEAD = auto()

class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()

class Slime(GameObject):
    def __init__(self, x=600, y=300):
        super().__init__(x, y, size=50)

        self.hp = 50
        self.speed = 80
        self.state = SlimeState.IDLE
        self.direction = Direction.LEFT
        self.agro = False  # HIT 상태인지 여부
        self.base_y = None  # 바닥(y) 저장
        self.vy = 0
        self.gravity = 1300
        self.on_ground = False

        rm = ResourceManager.instance()
        self.image_left = rm.get("Slime_Left")
        self.image_right = rm.get("Slime_Right")

        self.animations = {
            # IDLE
            (SlimeState.IDLE, Direction.LEFT):
                Animation(self.image_left, 100, 100,
                          {'x': 0, 'y': 400, 'frame_count': 3}),
            (SlimeState.IDLE, Direction.RIGHT):
                Animation(self.image_right, 100, 100,
                          {'x': 0, 'y': 400, 'frame_count': 3}),

            # HIT
            (SlimeState.HIT, Direction.LEFT):
                Animation(self.image_left, 100, 100,
                          {'x': 0, 'y': 300, 'frame_count': 1}),
            (SlimeState.HIT, Direction.RIGHT):
                Animation(self.image_right, 100, 100,
                          {'x': 0, 'y': 300, 'frame_count': 1}),

            # MOVE
            (SlimeState.MOVE, Direction.LEFT):
                Animation(self.image_left, 100, 100,
                          {'x': 0, 'y': 100, 'frame_count': 6}),
            (SlimeState.MOVE, Direction.RIGHT):
                Animation(self.image_right, 100, 100,
                          {'x': 0, 'y': 100, 'frame_count': 6}),

            # DEAD
            (SlimeState.DEAD, Direction.LEFT):
                Animation(self.image_left, 100, 100,
                          {'x': 0, 'y': 0, 'frame_count': 4}),
            (SlimeState.DEAD, Direction.RIGHT):
                Animation(self.image_right, 100, 100,
                          {'x': 0, 'y': 0, 'frame_count': 4}),
        }
        self.move_dir = 1  # -1 or 1
        self.move_timer = 0


    def update(self, dt):
        if self.is_dead:
            return

        self.apply_gravity(dt)

        self.ai(dt)
        self.animations[(self.state, self.direction)].update(dt)


    def ai(self, dt):
        if self.state == SlimeState.DEAD:
            return

        player = self.find_player()
        if player is None:
            return

        if self.state == SlimeState.HIT:
            self.chase_player(player, dt)
            return

        self.patrol(dt)

    def patrol(self, dt):
        self.move_timer += dt

        # 상태 전환 로직
        if self.state == SlimeState.MOVE:
            # 이동 중 2초 지나면 Idle로 전환
            if self.move_timer >= 2:
                self.state = SlimeState.IDLE
                self.move_timer = 0
                self.move_dir *= -1  # 이동 방향 반전
            else:

                dx = self.move_dir * self.speed * dt
                self.x += dx
                self.direction = Direction.LEFT if dx < 0 else Direction.RIGHT

        elif self.state == SlimeState.IDLE:

            if self.move_timer >= 3:
                self.state = SlimeState.MOVE
                self.move_timer = 0

    def chase_player(self, player, dt):
        if player.x < self.x:
            self.direction = Direction.LEFT
            self.x -= self.speed * dt * 1.4
        else:
            self.direction = Direction.RIGHT
            self.x += self.speed * dt * 1.4

        self.state = SlimeState.HIT


    def hit(self, dmg, attacker):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()
            return

        self.state = SlimeState.HIT

    def die(self):
        self.state = SlimeState.DEAD
        self.is_dead = True

    def apply_gravity(self, dt):
        # 바닥 위에 있으면 중력 적용 안함
        if self.on_ground:
            self.vy = 0
            return


        self.vy -= self.gravity * dt
        new_y = self.y + self.vy * dt

        foot_y = new_y - self.size / 2
        collided_y, collided = LineManager.instance().collision_line(self.x, foot_y, abs(self.vy * dt))

        if collided and self.vy <= 0:

            desired_foot_y = collided_y + 20
            self.y = desired_foot_y + self.size / 2
            self.vy = 0
            self.on_ground = True
        else:
            self.y = new_y
            self.on_ground = False

    def find_player(self):
        om = ObjectManager.instance()
        players = om.get_objects(OBJ.PLAYER)

        if len(players) == 0:
            return None
        return players[0]

    def render(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        anim = self.animations[(self.state, self.direction)]
        anim.draw(self.x, self.y, scroll_x, scroll_y)