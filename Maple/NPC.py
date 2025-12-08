from pico2d import *
from GameObject import GameObject
from Scroll_Manager import ScrollManager
from Resource_Manager import ResourceManager
from Animation_Manager import Animation
from enum import Enum, auto
from Input_Manager import Input_manager
import QuestData
from Portal import Portal
from Object_Manager import ObjectManager, OBJ
from Level_Manager import LEVEL_ID

class QuestIconState(Enum):
    NONE = auto()
    AVAILABLE = auto()
    IN_PROGRESS = auto()
    COMPLETE = auto()


class NPC(GameObject):
    def __init__(self, x=400, y=300):
        super().__init__(x, y, size=50)

        rm = ResourceManager.instance()
        self.chat_request = rm.get("CHAT1")
        self.chat_finish = rm.get("CHAT2")
        self.show_chat = False
        self.col_h = 70
        self.col_w = 50
        self.changeSound = load_wav("Resource/Sound/QuestClear.wav")
        self.changeSound.set_volume(32)
        self.quest_target = 20  # 슬라임 20마리 처치
        self.quest_kill_count = 0  # 현재 처치 수
        self.dialog_shown_after_complete = False  # 완료 후 대화창 표시 여부

        self.image = rm.get("NPC")
        self.animation = Animation(
            self.image, 50, 73,
            {'x': 0, 'y': 0, 'frame_count': 14}
        )

        self.icon_available = Animation(
            rm.get("Quest_Available"), 44, 46,
            {'x': 0, 'y': 0, 'frame_count': 8}
        )
        self.icon_in_progress = Animation(
            rm.get("Quest_Progress"), 42, 44,
            {'x': 0, 'y': 0, 'frame_count': 4}
        )
        self.icon_complete = Animation(
            rm.get("Quest_Complete"), 44, 44,
            {'x': 0, 'y': 0, 'frame_count': 8}
        )

        self.quest_state = QuestIconState.AVAILABLE

    def update(self, dt):
        if self.is_dead:
            return 1

        self.animation.update(dt)

        # 퀘스트 아이콘 애니메이션
        icon_anim = self.get_icon_anim()
        if icon_anim:
            icon_anim.update(dt)

        # 클릭 처리
        self.handle_click()

        # 대화창에서 엔터 처리
        if self.show_chat:
            self.handle_enter()

        if self.quest_state == QuestIconState.IN_PROGRESS and QuestData.global_quest_kill_count >= self.quest_target:
            self.quest_state = QuestIconState.COMPLETE
            self.changeSound.play()



    def render(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        self.animation.draw(self.x, self.y, scroll_x, scroll_y)
        icon_anim = self.get_icon_anim()
        if icon_anim:
            icon_anim.draw(self.x+10, self.y + 65, scroll_x, scroll_y)

        if self.show_chat:
            # 퀘스트 상태에 맞는 대화창 표시
            chat_img = self.chat_request if self.quest_state == QuestIconState.AVAILABLE else self.chat_finish
            chat_img.clip_draw(0, 0, chat_img.w, chat_img.h, self.x +200, self.y-100)



    def get_icon_anim(self):
        if self.quest_state == QuestIconState.AVAILABLE:
            return self.icon_available
        elif self.quest_state == QuestIconState.IN_PROGRESS:
            return self.icon_in_progress
        elif self.quest_state == QuestIconState.COMPLETE:
            return self.icon_complete
        return None

    def late_update(self):
        pass


    def release(self):
        pass

    def handle_click(self):
        im = Input_manager.instance()
        if im.Mouse_Down(SDL_BUTTON_LEFT):
            mx, my = im.Mouse_Pos()
            scroll_x, scroll_y = ScrollManager.instance().get_scroll()
            left = self.x - self.col_w // 2 - scroll_x
            right = self.x + self.col_w // 2 - scroll_x
            bottom = self.y - self.col_h // 2 - scroll_y
            top = self.y + self.col_h // 2 - scroll_y

            if left <= mx <= right and bottom <= my <= top:
                self.show_chat = True


    def handle_enter(self):
        """대화창이 켜진 상태에서 엔터 입력 시 퀘스트 상태 변경"""
        im = Input_manager.instance()
        if im.Key_Down(SDLK_RETURN):
            if self.quest_state == QuestIconState.AVAILABLE:
                self.quest_state = QuestIconState.IN_PROGRESS
            elif self.quest_state == QuestIconState.IN_PROGRESS:
                self.quest_state = QuestIconState.COMPLETE
            elif self.quest_state == QuestIconState.COMPLETE:
                self.quest_state = QuestIconState.NONE

            self.show_chat = False
            if self.quest_state == QuestIconState.NONE:
                self.is_dead = True

                portal = Portal(x=self.x, y=self.y, target_level=LEVEL_ID.LEVEL_BOSS)
                ObjectManager.instance().add_object(portal, OBJ.PORTAL)
