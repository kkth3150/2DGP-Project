from GameObject import GameObject
from enum import Enum, auto
from Resource_Manager import ResourceManager
from Animation_Manager import Animation
from Scroll_Manager import ScrollManager
from Object_Manager import ObjectManager, OBJ
from Damage import DamageNumber
import random
from pico2d import *

class BossState(Enum):
    IDLE = auto()
    MOVE = auto()
    ATTACK = auto()
    COOLDOWN = auto()
    DEAD = auto()

class BossAttackType(Enum):
    MELEE = auto()
    TELEPORT_SLASH = auto()
    ENERGY_BALL = auto()


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()

class Boss(GameObject):

    def __init__(self, x=800, y=400):
        super().__init__(x, y, size=120)

        self.max_hp =10000000
        self.hp = 10000000
        self.speed = 120
        self.state = BossState.IDLE
        self.direction = Direction.LEFT

        self.attack_cooldown = 2.5
        self.attack_timer = 0
        self.current_attack = None
        self.spell_casted = False
        rm = ResourceManager.instance()
        self.hitbox_width = 120  # 플레이어 공격 범위에 맞는 너비
        self.hitbox_height = 160  # 높이
        # -------------------- 기본 애니메이션 -------------------- #
        self.anim_idle_L = Animation(rm.get("Boss_Idle_L"), 130, 164, {'x':0,'y':0,'frame_count':6}, fps=6, loop=True)
        self.anim_idle_R = Animation(rm.get("Boss_Idle_R"), 130, 164, {'x':0,'y':0,'frame_count':6}, fps=6, loop=True)
        self.anim_move_L = Animation(rm.get("Boss_Walk_L"), 128, 163, {'x':0,'y':0,'frame_count':6}, fps=10, loop=True)
        self.anim_move_R = Animation(rm.get("Boss_Walk_R"), 128, 163, {'x':0,'y':0,'frame_count':6}, fps=10, loop=True)

        self.locked_animation = None

    # -------------------- 업데이트 -------------------- #
    def update(self, dt):
        if self.state == BossState.DEAD:
            return 1

        player = self.find_player()
        self.control_AI(player, dt)

        anim = self.select_animation()
        if anim:
            anim.update(dt)

        # 공격 종료 체크
        if self.state == BossState.ATTACK:
            if self.current_attack == BossAttackType.MELEE:
                # 마지막 프레임 직전에서 히트박스 생성
                last_frame_index = anim.frame_data['frame_count'] - 6
                if anim.frame_index == last_frame_index and not self.spell_casted:
                    self.spell_casted = True
                    if self.direction_locked == Direction.LEFT:
                        box_x = self.x - 60
                    else:
                        box_x = self.x + 60
                    box_y = self.y - 50
                    box = BossSkillBox(box_x, box_y, 90, 100)
                    ObjectManager.instance().add_object(box, OBJ.MONSTER_SKILLBOX)

            # 에너지볼 발사
            if self.current_attack == BossAttackType.ENERGY_BALL and not self.spell_casted:
                if anim.is_finished:
                    self.spell_casted = True
                    ball = EnergyBall(self.x, self.y - 50, self.direction_locked)
                    ObjectManager.instance().add_object(ball, OBJ.MONSTER)

            if self.current_attack == BossAttackType.TELEPORT_SLASH:
                last_frame_index = anim.frame_data['frame_count'] - 5  # 마지막 뒤 3프레임
                if anim.frame_index == last_frame_index and not self.spell_casted:
                    self.spell_casted = True  # 한 번만 생성
                    box_x = self.x
                    box_y = self.y - 155  # 필요하면 높이 조정
                    box = BossSkillBox(box_x, box_y, 2000, 20)  # 크기도 조정 가능
                    ObjectManager.instance().add_object(box, OBJ.MONSTER_SKILLBOX)

            if anim.is_finished:
                self.x, self.y = self.original_pos
                self.state = BossState.COOLDOWN
                self.spell_casted = False

        return 0

    # -------------------- 렌더링 -------------------- #
    def render(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        anim = self.select_animation()
        anim.draw(self.x, self.y, scroll_x, scroll_y)
        self.render_hitbox()

    # -------------------- AI -------------------- #
    def control_AI(self, player, dt):
        if not player or self.state == BossState.ATTACK:
            return

        dx = player.x - self.x
        distance = abs(dx)
        self.direction = Direction.RIGHT if dx > 0 else Direction.LEFT

        self.attack_timer += dt

        # ---- 쿨다운 중 ----
        if self.state == BossState.COOLDOWN:
            if self.attack_timer >= self.attack_cooldown:
                self.state = BossState.IDLE

        # ---- 공격 조건 ----
        if self.attack_timer >= self.attack_cooldown:
            if distance < 200:
                attack_choice = random.choice([ BossAttackType.MELEE,BossAttackType.ENERGY_BALL,
                                                BossAttackType.TELEPORT_SLASH])
                self.start_attack(attack_choice)
                return

        # ---- 이동 ----
        if distance > 300:
            self.state = BossState.MOVE
            self.x += (self.speed * dt) * (1 if dx > 0 else -1)
        else:
            self.state = BossState.IDLE

    def get_col_rect(self):
        w = self.hitbox_width / 2
        h = self.hitbox_height / 2
        return (self.x - w, self.y - h, self.x + w, self.y + h)

    # -------------------- 애니메이션 선택 -------------------- #
    def select_animation(self):
        if self.state == BossState.ATTACK:
            return self.locked_animation

        if self.state == BossState.MOVE:
            return self.anim_move_L if self.direction == Direction.LEFT else self.anim_move_R

        return self.anim_idle_L if self.direction == Direction.LEFT else self.anim_idle_R

    def hit(self, attacker, dmg=1000):
        if self.state == BossState.DEAD:
            return
        self.hp -= dmg
        ObjectManager.instance().add_object(DamageNumber(self.x, self.y + 150, dmg), OBJ.UI)

        if self.hp <= 0:
            self.state = BossState.DEAD

    def render_hitbox(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        x1, y1, x2, y2 = self.get_col_rect()
        draw_rectangle(x1 - scroll_x, y1 - scroll_y, x2 - scroll_x, y2 - scroll_y)
    # -------------------- 플레이어 찾기 -------------------- #
    def find_player(self):
        players = ObjectManager.instance().get_objects(OBJ.PLAYER)
        return players[0] if players else None

    # -------------------- 공격 시작 -------------------- #
    def start_attack(self, attack_type):
        self.state = BossState.ATTACK
        self.current_attack = attack_type
        self.attack_timer = 0

        self.original_pos = (self.x, self.y)
        self.direction_locked = self.direction
        self.spell_casted = False  # 에너지볼 발사 체크 초기화

        self.locked_animation = self.create_attack_animation()
        self.locked_animation.reset()

        self.apply_attack_offset()

    # -------------------- 공격 애니메이션 생성 -------------------- #
    def create_attack_animation(self):
        rm = ResourceManager.instance()

        if self.current_attack == BossAttackType.MELEE:
            img = rm.get("Boss_Melee_L") if self.direction_locked == Direction.LEFT else rm.get("Boss_Melee_R")
            return Animation(img, 2898 // 14, 237, {'x': 0, 'y': 0, 'frame_count': 14}, fps=12, loop=False)

        if self.current_attack == BossAttackType.ENERGY_BALL:
            img = rm.get("Boss_Spell_L") if self.direction_locked == Direction.LEFT else rm.get("Boss_Spell_R")
            return Animation(img, 7889 // 23, 287, {'x': 0, 'y': 0, 'frame_count': 23}, fps=10, loop=False)

        if self.current_attack == BossAttackType.TELEPORT_SLASH:  # 점프어택
            img = rm.get("Boss_Jump_L") if self.direction_locked == Direction.LEFT else rm.get("Boss_Jump_R")
            return Animation(img, 6608 // 16, 364, {'x': 0, 'y': 0, 'frame_count': 16}, fps=10, loop=False)

        return None

    # -------------------- 위치 이동 처리 -------------------- #
    def apply_attack_offset(self):
        offsets = {
            BossAttackType.MELEE: {
                Direction.LEFT: (-20, 35),
                Direction.RIGHT: (20, 35),
            },
            BossAttackType.ENERGY_BALL: {
                Direction.LEFT: (0, 30),
                Direction.RIGHT: (0, 30),
            },
            BossAttackType.TELEPORT_SLASH: {
                Direction.LEFT: (0, 90),
                Direction.RIGHT: (0, 90),
            }
        }

        # 현재 공격 타입이 offsets에 있으면 적용
        if self.current_attack not in offsets:
            return

        ox, oy = offsets[self.current_attack][self.direction_locked]
        self.x += ox
        self.y += oy
    # -------------------- 피격 처리 -------------------- #
    def hit(self, attacker, dmg=None):
        if self.state == BossState.DEAD:
            return

            # dmg가 지정되지 않으면 10000~30000 사이 랜덤
        if dmg is None:
            dmg = random.randint(10000, 30000)

        self.hp -= dmg
        ObjectManager.instance().add_object(DamageNumber(self.x-75, self.y + 150, dmg), OBJ.UI)

        if self.hp <= 0:
            self.state = BossState.DEAD

class EnergyBall(GameObject):
    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.speed = 150
        self.direction = direction
        rm = ResourceManager.instance()
        img = rm.get("EnergyBall_L") if direction == Direction.LEFT else rm.get("EnergyBall_R")
        self.anim = Animation(img, 548 // 4, 50, {'x':0,'y':0,'frame_count':4}, fps=8, loop=True)
        self.start_x = x
        self.max_distance = 500

        self.hitbox_created = False  # 히트박스 생성 여부
        self.has_collided = False   # 충돌 여부

    def update(self, dt):
        dx = -self.speed * dt if self.direction == Direction.LEFT else self.speed * dt
        self.x += dx
        self.anim.update(dt)

        # 최대 거리 넘어가면 삭제
        if abs(self.x - self.start_x) >= self.max_distance:
            return 1

        # 히트박스 생성
        if not self.has_collided:
            if self.direction == Direction.LEFT:
                box = BossSkillBox(self.x-40, self.y, 30, 30)
            else:
                box = BossSkillBox(self.x+40, self.y, 30, 30)
            ObjectManager.instance().add_object(box, OBJ.MONSTER_SKILLBOX)
            self.hitbox_created = True

        return 0

    def render(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        self.anim.draw(self.x, self.y, scroll_x, scroll_y)

class BossSkillBox(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, size=0)
        self.width = width
        self.height = height
        self.is_dead = False
        self.has_collided = False

    def update(self, dt):
        if self.has_collided or self.is_dead:
            self.is_dead = True
            return 1

        self.has_collided = True
        return 0

    def render(self):
        # 디버깅용 히트박스 표시
        scroll = ScrollManager.instance()
        scroll_x = scroll.scroll_x
        scroll_y = scroll.scroll_y
        draw_rectangle(self.x - self.width/2 - scroll_x,
                       self.y - self.height/2 - scroll_y,
                       self.x + self.width/2 - scroll_x,
                       self.y + self.height/2 - scroll_y)

    def get_col_rect(self):
        return (self.x - self.width/2,
                self.y - self.height/2,
                self.x + self.width/2,
                self.y + self.height/2)

    def hit(self, obj):
        pass
