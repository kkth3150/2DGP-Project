from Object_Manager import ObjectManager, OBJ
from Resource_Manager import ResourceManager
from Scroll_Manager import ScrollManager
from Line_Manager import LineManager, Line
from Player import Player
from Default_UI import Default_UI, UI_INDEX
from Slime import Slime

class level_tutorial:
    def __init__(self):
        self.bg_key = "Tutorial_Map"
        self.bg_path = "Resource/Map/Skill_Field.png"  # 배경 이미지 경로
        self.bg_image = None

    def initialize(self):
        rm = ResourceManager.instance()
        rm.load(self.bg_key, self.bg_path)
        rm.load("Player_Left","Resource/Player/Player_Left.png")
        rm.load("Player_Right", "Resource/Player/Player_Right.png")
        rm.load("UI_EXP_BAR","Resource/UI/EXPBar.png")
        rm.load("Inventory", "Resource/UI/Inventory_Small.png")

        rm.load("Slime_Left","Resource/Monster/SlimLeft.png")
        rm.load("Slime_Right", "Resource/Monster/SlimRight.png")

        self.bg_image = rm.get(self.bg_key)

        ground_line1 = Line(0, 210, self.bg_image.w, 210, thickness=5)
        LineManager.instance().add_line(ground_line1)

        ground_line2 = Line(280, 450, self.bg_image.w-180, 450, thickness=5)
        LineManager.instance().add_line(ground_line2)

        small_ground_line1 = Line(105,335,230,335,thickness=5)
        LineManager.instance().add_line(small_ground_line1)

        small_ground_line2 = Line(105,400,230,400,thickness=5)
        LineManager.instance().add_line(small_ground_line2)


        ObjectLine2 = Line(272,270,372,270,thickness=5)
        LineManager.instance().add_line(ObjectLine2)


        players = ObjectManager.instance().get_objects(OBJ.PLAYER)
        if not players:
            player = Player(x=300, y=400)
            ObjectManager.instance().add_object(player, OBJ.PLAYER)

        slime1 = Slime(x=500, y=600)  # 위쪽 라인 근처 → 떨어져서 착지
        ObjectManager.instance().add_object(slime1, OBJ.MONSTER)

        exp_ui = Default_UI(UI_INDEX.EXP_BAR, player=player, x=400, y=40)
        ObjectManager.instance().add_object(exp_ui, OBJ.UI)

    def update(self,dt):
        ObjectManager.instance().update(dt)

    def late_update(self):
        ObjectManager.instance().late_update()

    def render(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        if self.bg_image:
            self.bg_image.clip_draw(0, 0,
                                    self.bg_image.w, self.bg_image.h,
                                    self.bg_image.w // 2 - scroll_x,
                                    self.bg_image.h // 2 - scroll_y)
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        LineManager.instance().render(scroll_x, scroll_y)
        ObjectManager.instance().render()



    def release(self):
        ObjectManager.instance().release_all_except([OBJ.PLAYER])