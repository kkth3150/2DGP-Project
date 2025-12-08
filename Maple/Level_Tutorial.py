from pico2d import load_music

from Object_Manager import ObjectManager, OBJ
from Resource_Manager import ResourceManager
from Scroll_Manager import ScrollManager
from Line_Manager import LineManager, Line
from Player import Player
from Default_UI import Default_UI, UI_INDEX
from Slime import Slime
from NPC import NPC


class level_tutorial:
    def __init__(self):
        self.bg_key = "Tutorial_Map"
        self.bg_path = "Resource/Map/Skill_Field.png"  # 배경 이미지 경로
        self.bg_image = None
        self.slime_positions = [
            (200, 300), (400, 300), (600, 300), (800, 300), (1000, 300),
            (280, 500), (480, 500), (580, 500), (680, 500), (880, 500)
        ]
        self.spawn_interval = 1.0  # 1초마다 한 마리씩 스폰
        self.time_since_last_spawn = 0.0
        self.next_slime_index = 0  # 다음에 생성할 위치 인덱스
        self.bgm = load_music("Resource/Sound/FloralLife.mp3")
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def initialize(self):
        self.load_resources()
        self.create_lines()
        self.create_objects()


    def update(self,dt):
        ObjectManager.instance().update(dt)
        self.time_since_last_spawn += dt

        current_slimes = ObjectManager.instance().get_objects(OBJ.MONSTER)
        if len(current_slimes) < 10 and self.time_since_last_spawn >= self.spawn_interval:
            self.spawn_one_slime()
            self.time_since_last_spawn = 0.0

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
        ObjectManager.instance().clear_objects(OBJ.MONSTER)
        ObjectManager.instance().clear_objects(OBJ.ITEM)
        ObjectManager.instance().clear_objects(OBJ.NPC)
        ObjectManager.instance().clear_objects(OBJ.PORTAL)
        LineManager.instance().clear()

    def load_resources(self):
        rm = ResourceManager.instance()

        rm.load(self.bg_key, self.bg_path)
        rm.load("Player_Left", "Resource/Player/Player_Left.png")
        rm.load("Player_Right", "Resource/Player/Player_Right.png")
        rm.load("UI_EXP_BAR", "Resource/UI/EXPBar.png")
        rm.load("Inventory", "Resource/UI/Inventory_Small.png")
        rm.load("Hp_Bar","Resource/UI/hp.png")

        rm.load("Slime_Left", "Resource/Monster/SlimLeft.png")
        rm.load("Slime_Right", "Resource/Monster/SlimRight.png")

        rm.load("NPC", "Resource/NPC/NPC.png")
        rm.load("Quest_Available", "Resource/NPC/Quest1.png")
        rm.load("Quest_Progress", "Resource/NPC/Quest2.png")
        rm.load("Quest_Complete", "Resource/NPC/Quest3.png")

        rm.load("Num_0","Resource/UI/Num/0.png")
        rm.load("Num_1","Resource/UI/Num/1.png")
        rm.load("Num_2","Resource/UI/Num/2.png")
        rm.load("Num_3","Resource/UI/Num/3.png")
        rm.load("Num_4","Resource/UI/Num/4.png")
        rm.load("Num_5","Resource/UI/Num/5.png")
        rm.load("Num_6","Resource/UI/Num/6.png")
        rm.load("Num_7","Resource/UI/Num/7.png")
        rm.load("Num_8","Resource/UI/Num/8.png")
        rm.load("Num_9","Resource/UI/Num/9.png")
        rm.load("Critical","Resource/UI/Num/critical.png")

        rm.load("Swing1_L","Resource/Effect/Attack/Swing1L.png")
        rm.load("Swing1_R", "Resource/Effect/Attack/Swing1R.png")
        rm.load("Swing2_L","Resource/Effect/Attack/Swing2L.png")
        rm.load("Swing2_R","Resource/Effect/Attack/Swing2R.png")
        rm.load("Swing3_L","Resource/Effect/Attack/Swing3L.png")
        rm.load("Swing3_R", "Resource/Effect/Attack/Swing3R.png")

        rm.load("Beyonder1_L", "Resource/Effect/Attack/Beyond1L.png")
        rm.load("Beyonder1_R", "Resource/Effect/Attack/Beyond1R.png")
        rm.load("Beyonder2_L","Resource/Effect/Attack/Beyond2L.png")
        rm.load("Beyonder2_R", "Resource/Effect/Attack/Beyond2R.png")
        rm.load("Beyonder3_L","Resource/Effect/Attack/Beyond3L.png")
        rm.load("Beyonder3_R", "Resource/Effect/Attack/Beyond3R.png")
        rm.load("Beyonder4_L","Resource/Effect/Attack/Beyond4L.png")
        rm.load("Beyonder4_R", "Resource/Effect/Attack/Beyond4R.png")

        rm.load("Potion","Resource/Item/Item_Potion.png")

        rm.load("Portal","Resource/UI/potal.png")

        rm.load("CHAT1","Resource/NPC/request.png")
        rm.load("CHAT2", "Resource/NPC/finish.png")

        rm.load("Win","Resource/NPC/Win.png")
        rm.load("Lose","Resource/NPC/Lose.png")

        self.bg_image = rm.get(self.bg_key)

    def create_lines(self):
        lm = LineManager.instance()

        lm.add_line(Line(0, 210, self.bg_image.w, 210, thickness=5))
        lm.add_line(Line(280, 450, self.bg_image.w - 180, 450, thickness=5))

        lm.add_line(Line(105, 335, 230, 335, thickness=5))
        lm.add_line(Line(105, 400, 230, 400, thickness=5))

        lm.add_line(Line(272, 270, 372, 270, thickness=5))

    def spawn_one_slime(self):
        if self.next_slime_index >= len(self.slime_positions):
            self.next_slime_index = 0  # 순환 가능

        pos = self.slime_positions[self.next_slime_index]
        slime = Slime(x=pos[0], y=pos[1])
        ObjectManager.instance().add_object(slime, OBJ.MONSTER)

        self.next_slime_index += 1

    def create_objects(self):
        om = ObjectManager.instance()

        players = om.get_objects(OBJ.PLAYER)
        if not players:
            player = Player(x=300, y=600)
            om.add_object(player, OBJ.PLAYER)
        else:
            player = players[0]

        # 몬스터
        slime1 = Slime(x=500, y=600)
        om.add_object(slime1, OBJ.MONSTER)

        # NPC
        npc = NPC(x=165, y=430)
        om.add_object(npc, OBJ.NPC)

        # UI
        exp_ui = Default_UI(UI_INDEX.EXP_BAR, player=player, x=400, y=40)
        om.add_object(exp_ui, OBJ.UI)

        hp_ui = Default_UI(UI_INDEX.HP_BAR, player=player, x=407, y=41)
        om.add_object(hp_ui, OBJ.UI)

