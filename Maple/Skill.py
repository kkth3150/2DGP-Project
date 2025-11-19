from GameObject import GameObject
from Scroll_Manager import ScrollManager
from Resource_Manager import ResourceManager
from enum import Enum, auto
from Object_Manager import ObjectManager
from Animation_Manager import SkillAnimation


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
            self.offset_x = 0  # C++ 좌측 보정
            self.offset_y = 0

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
            self.offset_x = 0  # C++ 우측 보정
            self.offset_y = 0

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
            self.offset_x = 0  # C++ 좌측 보정
            self.offset_y = 0

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
            self.offset_x = 0  # C++ 우측 보정
            self.offset_y = 0