from Object_Manager import ObjectManager, OBJ
from Resource_Manager import ResourceManager
from Scroll_Manager import ScrollManager
from Line_Manager import LineManager, Line
from Player import Player
from Default_UI import Default_UI, UI_INDEX
from Slime import Slime
from NPC import NPC    # ← NPC 불러오기!
from Portal import Portal
from Level_Manager import LEVEL_ID
from Boss import Boss
from pico2d import *

class level_boss:
    def __init__(self):
        self.bg_key = "Boss_Map"
        self.bg_path = "Resource/Map/BossField.png"  # 배경 이미지 경로
        self.bg_image = None
        self.bgm = load_music("Resource/Sound/TimeChaos.mp3")
        self.bgm.set_volume(32)
        self.bgm.repeat_play()
        ObjectManager.instance().clear_objects(OBJ.MONSTER)



    def initialize(self):
        self.load_resources()
        self.create_lines()
        self.create_objects()
        self.change_objects()


    def update(self,dt):
        ObjectManager.instance().update(dt)

    def late_update(self):
        ObjectManager.instance().late_update()

    def render(self):
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()

        if self.bg_image:
            self.bg_image.clip_draw(
                0, 0,
                self.bg_image.w, self.bg_image.h,
                self.bg_image.w // 2 - scroll_x,
                self.bg_image.h // 2 - scroll_y
            )

        LineManager.instance().render(scroll_x, scroll_y)
        ObjectManager.instance().render()

    def release(self):
        pass

    def load_resources(self):
        rm = ResourceManager.instance()
        rm.load(self.bg_key, self.bg_path)
        self.bg_image = rm.get(self.bg_key)

        rm.load("Boss_Idle_L", "Resource/Boss/L/IdleL.png")
        rm.load("Boss_Idle_R", "Resource/Boss/R/IdleR.png")

        rm.load("Boss_Walk_L","Resource/Boss/L/WalkL.png")
        rm.load("Boss_Walk_R","Resource/Boss/R/WalkR.png")

        rm.load("Boss_Melee_L", "Resource/Boss/L/Attack1L.png")
        rm.load("Boss_Melee_R", "Resource/Boss/R/Attack1R.png")

        rm.load("Boss_Spell_L", "Resource/Boss/L/Attack2L.png")
        rm.load("Boss_Spell_R", "Resource/Boss/R/Attack2R.png")

        rm.load("EnergyBall_L", "Resource/Boss/L/BallL.png")
        rm.load("EnergyBall_R","Resource/Boss/R/BallR.png")

        rm.load("Boss_Jump_L","Resource/Boss/L/Attack3L.png")
        rm.load("Boss_Jump_R","Resource/Boss/R/Attack3R.png")


    def create_lines(self):
        lm = LineManager.instance()
        lm.add_line(Line(0, 80, self.bg_image.w, 80, thickness=5))

    def create_objects(self):
        om = ObjectManager.instance()

        # === 보스 생성 추가 ===
        boss = Boss(x=800, y=150)
        om.add_object(boss, OBJ.BOSS)

        bossHp = Default_UI(UI_INDEX.BOSS_HP_BAR, x=400, y=600)
        om.add_object(bossHp, OBJ.UI)

    def change_objects(self):
        om = ObjectManager.instance()
        players = om.get_objects(OBJ.PLAYER)

        if players:
            player = players[0]
            player.x = 50
            player.y = 200
        else:
            player = Player(x=200, y=120)
            om.add_object(player, OBJ.PLAYER)