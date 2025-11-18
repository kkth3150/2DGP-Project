from pico2d import *
from GameObject import GameObject
from Scroll_Manager import ScrollManager
from Resource_Manager import ResourceManager
from Animation_Manager import Animation
from enum import Enum, auto
from Input_Manager import Input_manager


class QuestIconState(Enum):
    NONE = auto()          # 아이콘 없음
    AVAILABLE = auto()     # 퀘스트 수령 가능 (!)
    IN_PROGRESS = auto()   # 진행 중 (…)
    COMPLETE = auto()      # 완료 (✔)


class NPC(GameObject):
    def __init__(self, x=400, y=300):
        super().__init__(x, y, size=50)

        rm = ResourceManager.instance()

        self.col_h = 70
        self.col_w = 50

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

        self.animation.update(dt)

        icon_anim = self.get_icon_anim()
        if icon_anim:
            icon_anim.update(dt)
        self.handle_click()

    def render(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()

        self.animation.draw(self.x, self.y, scroll_x, scroll_y)

        icon_anim = self.get_icon_anim()
        if icon_anim:
            icon_anim.draw(self.x+10, self.y + 65, scroll_x, scroll_y)

        draw_rectangle(
            self.x - self.col_w // 2 - scroll_x,
            self.y - self.col_h // 2 - scroll_y,
            self.x + self.col_w // 2 - scroll_x,
            self.y + self.col_h // 2 - scroll_y
        )

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
            # NPC 기준 스크롤 적용
            left = self.x - self.col_w // 2 - scroll_x
            right = self.x + self.col_w // 2 - scroll_x
            bottom = self.y - self.col_h // 2 - scroll_y
            top = self.y + self.col_h // 2 - scroll_y

            if left <= mx <= right and bottom <= my <= top:
                # 클릭 시 퀘스트 상태 변경 (순환)
                if self.quest_state == QuestIconState.AVAILABLE:
                    self.quest_state = QuestIconState.IN_PROGRESS
                elif self.quest_state == QuestIconState.IN_PROGRESS:
                    self.quest_state = QuestIconState.COMPLETE
                elif self.quest_state == QuestIconState.COMPLETE:
                    self.quest_state = QuestIconState.NONE
                else:
                    self.quest_state = QuestIconState.AVAILABLE