from Object_Manager import ObjectManager, OBJ
from Resource_Manager import ResourceManager
from Scroll_Manager import ScrollManager
from Line_Manager import LineManager, Line
from Player import Player

class level_tutorial:
    def __init__(self):
        self.bg_key = "Tutorial_Map"
        self.bg_path = "Resource/Map/Skill_Field.png"  # 배경 이미지 경로
        self.bg_image = None

    def initialize(self):
        rm = ResourceManager.instance()
        rm.load(self.bg_key, self.bg_path)
        self.bg_image = rm.get(self.bg_key)

        ground_line = Line(0, 210, self.bg_image.w, 210, thickness=5)
        LineManager.instance().add_line(ground_line)
        players = ObjectManager.instance().get_objects(OBJ.PLAYER)
        if not players:
            player = Player(x=300, y=300)
            ObjectManager.instance().add_object(player, OBJ.PLAYER)

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

        ObjectManager.instance().render()
        scroll_x, scroll_y = ScrollManager.instance().get_scroll()
        LineManager.instance().render(scroll_x, scroll_y)

    def release(self):
        ObjectManager.instance().release_all_except([OBJ.PLAYER])