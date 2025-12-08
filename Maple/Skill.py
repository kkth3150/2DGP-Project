from GameObject import GameObject
from Scroll_Manager import ScrollManager
from Resource_Manager import ResourceManager
from enum import Enum, auto
from Object_Manager import ObjectManager, OBJ
from Animation_Manager import SkillAnimation
from pico2d import *

class Skill_Kind(Enum):
    NONE = auto()

    Swing1_L = auto()
    Swing1_R = auto()
    Swing2_L = auto()
    Swing2_R = auto()
    Swing3_L = auto()
    Swing3_R = auto()

    Beyond1_L = auto()
    Beyond1_R = auto()
    Beyond2_L = auto()
    Beyond2_R = auto()
    Beyond3_L = auto()
    Beyond3_R = auto()
    Beyond4_L = auto()
    Beyond4_R = auto()


class Skill(GameObject):

    def __init__(self, x, y, skill_kind: Skill_Kind):
        super().__init__(x, y, size=0)
        self.skill_kind = skill_kind
        self.is_dead = False
        self.anim = None
        self.offset_x = 0
        self.offset_y = 0
        self.setup_skill()

    def update(self, dt):
        if self.is_dead:
            return 1

        self.anim.update(dt)

        if self.anim.is_finished:
            self.is_dead = True

    def render(self):
        scroll = ScrollManager.instance()
        scroll_x = scroll.scroll_x
        scroll_y = scroll.scroll_y

        self.anim.draw(
            self.x,
            self.y,
            scroll_x,
            scroll_y,
            offset_x=self.offset_x,
            offset_y=self.offset_y
        )

    def setup_skill(self):
        rm = ResourceManager.instance()
        if self.skill_kind == Skill_Kind.Swing1_L:
            img = rm.get("Swing1_L")
            self.anim = SkillAnimation(
                image=img,
                frame_width=280,
                frame_height=232,
                frame_count=5,  # 프레임 수 5개
                change_speed=0.05,  # 50ms
                loop=False
            )
            # C++ 기준 위치 보정
            self.offset_x = -50
            self.offset_y = -28
            width, height = 150, 150  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x-10, self.y + self.offset_y+25, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        elif self.skill_kind == Skill_Kind.Swing1_R:
            img = rm.get("Swing1_R")
            self.anim = SkillAnimation(
                image=img,
                frame_width=280,
                frame_height=232,
                frame_count=5,
                change_speed=0.05,
                loop=False
            )
            self.offset_x = +50
            self.offset_y = -28
            width, height = 150, 150  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x+10, self.y + self.offset_y+25, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        elif self.skill_kind == Skill_Kind.Swing2_L:
            img = rm.get("Swing2_L")
            self.anim = SkillAnimation(
                image=img,
                frame_width=294,  # C++ 기준 m_iRenderWidth
                frame_height=157,  # m_iRenderHeight
                frame_count=5,
                change_speed=0.05,
                loop=False
            )
            self.offset_x =0
            self.offset_y = 0
            width, height = 260, 150  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x, self.y + self.offset_y, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        elif self.skill_kind == Skill_Kind.Swing2_R:
            img = rm.get("Swing2_R")
            self.anim = SkillAnimation(
                image=img,
                frame_width=294,
                frame_height=157,
                frame_count=5,
                change_speed=0.05,
                loop=False
            )
            self.offset_x = 0  # R도 동일하게 C++에서 -144 보정
            self.offset_y = 0
            width, height = 260, 150  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x, self.y + self.offset_y, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        elif self.skill_kind == Skill_Kind.Swing3_L:
            img = rm.get("Swing3_L")
            self.anim = SkillAnimation(
                image=img,
                frame_width=462,  # C++ m_iRenderWidth
                frame_height=399,  # C++ m_iRenderHeight
                frame_count=7,
                change_speed=0.05,
                loop=False
            )
            self.offset_x = -30
            self.offset_y = 0
            width, height = 180, 230  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x-50, self.y + self.offset_y, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        elif self.skill_kind == Skill_Kind.Swing3_R:
            img = rm.get("Swing3_R")
            self.anim = SkillAnimation(
                image=img,
                frame_width=462,
                frame_height=399,
                frame_count=7,
                change_speed=0.05,
                loop=False
            )
            self.offset_x = +30
            self.offset_y = 0
            width, height = 180, 230  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x+50, self.y + self.offset_y, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        elif self.skill_kind == Skill_Kind.Beyond1_L:
            img = rm.get("Beyonder1_L")
            self.anim = SkillAnimation(
                image=img,
                frame_width=588,  # C++ m_iRenderWidth
                frame_height=472,  # C++ m_iRenderHeight
                frame_count=10,  # 스프라이트 10개
                change_speed=0.05,  # 50ms
                loop=False
            )
            self.offset_x = -120  # C++ 좌측 보정
            self.offset_y = 100
            width, height = 300, 200  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x-40, self.y + self.offset_y-70, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        elif self.skill_kind == Skill_Kind.Beyond1_R:
            img = rm.get("Beyonder1_R")
            self.anim = SkillAnimation(
                image=img,
                frame_width=588,
                frame_height=472,
                frame_count=10,
                change_speed=0.05,
                loop=False
            )
            self.offset_x = 120  # C++ 우측 보정
            self.offset_y = 100
            width, height = 300, 200  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x+40, self.y + self.offset_y-70, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        # ---- Beyond2 / Beyonder2 ----
        elif self.skill_kind == Skill_Kind.Beyond2_L:
            img = rm.get("Beyonder2_L")
            self.anim = SkillAnimation(
                image=img,
                frame_width=586,  # C++ m_iRenderWidth
                frame_height=530,  # C++ m_iRenderHeight
                frame_count=14,  # 스프라이트 14개
                change_speed=0.05,  # 50ms
                loop=False
            )
            self.offset_x = -50  # C++ 좌측 보정
            self.offset_y = 130
            width, height = 250, 250  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x-100, self.y + self.offset_y-100, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        elif self.skill_kind == Skill_Kind.Beyond2_R:
            img = rm.get("Beyonder2_R")
            self.anim = SkillAnimation(
                image=img,
                frame_width=586,
                frame_height=530,
                frame_count=14,
                change_speed=0.05,
                loop=False
            )
            self.offset_x = 50  # C++ 우측 보정
            self.offset_y = 130

            width, height = 250, 250  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x+100, self.y + self.offset_y-100, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        elif self.skill_kind == Skill_Kind.Beyond3_L:
            img = rm.get("Beyonder3_L")
            self.anim = SkillAnimation(
                image=img,
                frame_width=475,  # C++ m_iRenderWidth
                frame_height=499,  # C++ m_iRenderHeight
                frame_count=14,  # 스프라이트 14개
                change_speed=0.05,  # 50ms
                loop=False
            )
            self.offset_x = -50  # C++ 좌측 보정
            self.offset_y = 130
            width, height = 300, 250  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x-50, self.y + self.offset_y-100, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        elif self.skill_kind == Skill_Kind.Beyond3_R:
            img = rm.get("Beyonder3_R")
            self.anim = SkillAnimation(
                image=img,
                frame_width=475,
                frame_height=499,
                frame_count=14,
                change_speed=0.05,
                loop=False
            )
            self.offset_x = 50  # C++ 우측 보정
            self.offset_y = 130
            width, height = 300, 250  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x+50 , self.y + self.offset_y-100, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        elif self.skill_kind == Skill_Kind.Beyond4_L:
            img = rm.get("Beyonder4_L")
            self.anim = SkillAnimation(
                image=img,
                frame_width=737,  # 11059 ÷ 15 = 737
                frame_height=603,
                frame_count=15,
                change_speed=0.05,
                loop=False
            )
            self.offset_x = -50  # 좌측 보정, 필요 시 조정
            self.offset_y = 130  # 위/아래 보정, 필요 시 조정
            width, height = 350, 250  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x-100, self.y + self.offset_y-100, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

        elif self.skill_kind == Skill_Kind.Beyond4_R:
            img = rm.get("Beyonder4_R")
            self.anim = SkillAnimation(
                image=img,
                frame_width=737,
                frame_height=603,
                frame_count=15,
                change_speed=0.05,
                loop=False
            )
            self.offset_x = 50  # 우측 보정
            self.offset_y = 130
            width, height = 350, 250  # 실제 스킬 범위에 맞춰 설정
            hitbox = PlayerSkillBox(self.x + self.offset_x+100, self.y + self.offset_y-100, width, height)
            ObjectManager.instance().add_object(hitbox, OBJ.PLAYER_SKILLBOX)

class PlayerSkillBox(GameObject):
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


    def get_col_rect(self):
        return (self.x - self.width/2,
                self.y - self.height/2,
                self.x + self.width/2,
                self.y + self.height/2)

    def hit(self, obj):
        pass
