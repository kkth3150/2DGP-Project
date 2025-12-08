from GameObject import GameObject
from enum import Enum, auto
from Resource_Manager import ResourceManager
from Animation_Manager import Animation
from Scroll_Manager import ScrollManager
from Object_Manager import ObjectManager, OBJ
from Damage import DamageNumber
import random

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

        self.hp = 100000
        self.speed = 120
        self.state = BossState.IDLE
        self.direction = Direction.LEFT

        self.attack_cooldown = 2.5
        self.attack_timer = 0
        self.current_attack = None
        self.spell_casted = False
        rm = ResourceManager.instance()

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
            # 에너지볼 발사
            if self.current_attack == BossAttackType.ENERGY_BALL and not self.spell_casted:
                if anim.is_finished:
                    self.spell_casted = True
                    ball = EnergyBall(self.x, self.y - 50, self.direction_locked)
                    ObjectManager.instance().add_object(ball, OBJ.MONSTER)

            # # 점프어택 마지막 프레임에서 플레이어 피격
            # if self.current_attack == BossAttackType.TELEPORT_SLASH:
            #     if anim.is_finished and player and not player.is_jumping:  # player.is_jumping 필요
            #         player.hit(500)  # 예: HP 500 감소

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

    # -------------------- 애니메이션 선택 -------------------- #
    def select_animation(self):
        if self.state == BossState.ATTACK:
            return self.locked_animation

        if self.state == BossState.MOVE:
            return self.anim_move_L if self.direction == Direction.LEFT else self.anim_move_R

        return self.anim_idle_L if self.direction == Direction.LEFT else self.anim_idle_R

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
    def hit(self, attacker, dmg=1000):
        if self.state == BossState.DEAD:
            return

        self.hp -= dmg
        ObjectManager.instance().add_object(DamageNumber(self.x, self.y + 150, dmg), OBJ.UI)

        if self.hp <= 0:
            self.state = BossState.DEAD

class EnergyBall(GameObject):
    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.speed = 150  # 천천히 이동
        self.direction = direction
        rm = ResourceManager.instance()
        img = rm.get("EnergyBall_L") if direction == Direction.LEFT else rm.get("EnergyBall_R")
        self.anim = Animation(img, 548 // 4, 50, {'x':0,'y':0,'frame_count':4}, fps=8, loop=True)
        self.start_x = x
        self.max_distance = 500  # 특정 거리 이상 날아가면 삭제

    def update(self, dt):
        dx = -self.speed * dt if self.direction == Direction.LEFT else self.speed * dt
        self.x += dx
        self.anim.update(dt)

        if abs(self.x - self.start_x) >= self.max_distance:
            return 1

        return 0

    def render(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        self.anim.draw(self.x, self.y, scroll_x, scroll_y)