from GameObject import GameObject
from enum import Enum, auto
from Resource_Manager import ResourceManager
from Animation_Manager import Animation
from Scroll_Manager import ScrollManager
from Object_Manager import ObjectManager, OBJ
from Line_Manager import LineManager
from pico2d import *
from Damage import DamageNumber
from Item import DropItem
import QuestData
from NPC import NPC, QuestIconState

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

        self.hp = 10000
        self.speed = 50
        self.state = SlimeState.IDLE
        self.direction = Direction.LEFT
        self.agro = False
        self.vy = 0
        self.gravity = 1300
        self.ground_offset = 20
        self.on_ground = False
        self.hit_timer = 0
        self.hit_duration = 0.2

        rm = ResourceManager.instance()
        self.image_left = rm.get("Slime_Left")
        self.image_right = rm.get("Slime_Right")

        self.animations = {
            (SlimeState.IDLE, Direction.LEFT):
                Animation(self.image_left, 100, 100, {'x':0,'y':400,'frame_count':3}, fps=8, loop=True),
            (SlimeState.IDLE, Direction.RIGHT):
                Animation(self.image_right, 100, 100, {'x':0,'y':400,'frame_count':3}, fps=8, loop=True),
            (SlimeState.HIT, Direction.LEFT):
                Animation(self.image_left, 100, 100, {'x':0,'y':300,'frame_count':1}, fps=8, loop=False),
            (SlimeState.HIT, Direction.RIGHT):
                Animation(self.image_right, 100, 100, {'x':0,'y':300,'frame_count':1}, fps=8, loop=False),
            (SlimeState.MOVE, Direction.LEFT):
                Animation(self.image_left, 100, 100, {'x':0,'y':100,'frame_count':6}, fps=8, loop=True),
            (SlimeState.MOVE, Direction.RIGHT):
                Animation(self.image_right, 100, 100, {'x':0,'y':100,'frame_count':6}, fps=8, loop=True),
            (SlimeState.DEAD, Direction.LEFT):
                Animation(self.image_left, 100, 100, {'x':0,'y':0,'frame_count':4}, fps=8, loop=False),
            (SlimeState.DEAD, Direction.RIGHT):
                Animation(self.image_right, 100, 100, {'x':0,'y':0,'frame_count':4}, fps=8, loop=False),
        }

        self.move_dir = 1
        self.move_timer = 0
        self.is_dead = False

    def update(self, dt):
        if self.is_dead:
            return 1

        anim = self.animations[(self.state, self.direction)]
        anim.update(dt)

        if self.state == SlimeState.DEAD:
            if anim.is_finished:
                self.is_dead = True
                return 1  # 객체 삭제 신호
            return


        self.apply_gravity(dt)
        player = self.find_player()


        if self.state == SlimeState.HIT:
            self.hit_timer += dt
            if self.hit_timer >= self.hit_duration:
                self.hit_timer = 0
                if self.hp > 0:
                    self.state = SlimeState.IDLE
                    self.agro = True


        if self.agro and player:
            self.chase_or_idle(player, dt)
        else:
            if self.state != SlimeState.HIT:
                self.patrol(dt)


    def chase_or_idle(self, player, dt):
        dx = player.x - self.x
        min_distance = 50
        if abs(dx) > min_distance:
            move_amount = min(self.speed * dt, abs(dx) - min_distance)
            self.x += move_amount if dx > 0 else -move_amount
            self.direction = Direction.RIGHT if dx > 0 else Direction.LEFT
            if self.state != SlimeState.HIT:
                self.state = SlimeState.MOVE
        else:
            if self.state != SlimeState.HIT:
                self.state = SlimeState.IDLE

    def patrol(self, dt):
        self.move_timer += dt
        if self.state == SlimeState.MOVE:
            if self.move_timer >= 2:
                self.state = SlimeState.IDLE
                self.move_timer = 0
                self.move_dir *= -1
            else:
                dx = self.move_dir * self.speed * dt
                self.x += dx
                self.direction = Direction.LEFT if dx < 0 else Direction.RIGHT
        elif self.state == SlimeState.IDLE:
            if self.move_timer >= 3:
                self.state = SlimeState.MOVE
                self.move_timer = 0

    def chase_player(self, player, dt):
        min_distance = 30
        dx = player.x - self.x
        if abs(dx) > min_distance:
            move_amount = min(self.speed * dt, abs(dx) - min_distance)
            self.x += move_amount if dx > 0 else -move_amount
            self.direction = Direction.RIGHT if dx > 0 else Direction.LEFT

    def hit(self, attacker, dmg=99999):
        if self.is_dead:
            return

        self.hp -= dmg
        dmg_num = DamageNumber(self.x - 100, self.y + 50, dmg, critical=False)
        ObjectManager.instance().add_object(dmg_num, OBJ.EFFECT)

        if self.hp <= 0:
            self.die()
            return


        self.state = SlimeState.HIT
        self.hit_timer = 0
        self.agro = True

    def die(self):
        self.state = SlimeState.DEAD
        self.vx = 0
        self.vy = 0
        potion = DropItem(self.x, self.y - 30)
        ObjectManager.instance().add_object(potion, OBJ.ITEM)  # or OBJ.ITEM
        npcs = ObjectManager.instance().get_objects(OBJ.NPC)
        if npcs:
            npc = npcs[0]
            if npc.quest_state == QuestIconState.IN_PROGRESS:
                # 기존의 from QuestData import global_quest_kill_count 는 사용하지 말고
                QuestData.global_quest_kill_count += 1  # <- 이렇게 모듈명을 명시해야 글로벌 변수가 제대로 증가
    def apply_gravity(self, dt):
        self.vy -= self.gravity * dt
        new_y = self.y + self.vy * dt
        foot_y = new_y - self.size / 2 - self.ground_offset
        collided_y, collided = LineManager.instance().collision_line(self.x, foot_y, abs(self.vy * dt))
        if collided and self.vy <= 0:
            self.y = (collided_y + self.ground_offset) + self.size / 2
            self.vy = 0
            self.on_ground = True
        else:
            self.y = new_y
            self.on_ground = False

    def find_player(self):
        players = ObjectManager.instance().get_objects(OBJ.PLAYER)
        return players[0] if players else None

    def render(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        anim = self.animations[(self.state, self.direction)]
        anim.draw(self.x, self.y, scroll_x, scroll_y)

    def get_col_rect(self):
        width = 70
        height = 50
        return (self.x - width/2, self.y - height/2-25, self.x + width/2, self.y + height/2-25)

    def render_hitbox(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        x1, y1, x2, y2 = self.get_col_rect()
        draw_rectangle(x1 - scroll_x, y1 - scroll_y, x2 - scroll_x, y2 - scroll_y)