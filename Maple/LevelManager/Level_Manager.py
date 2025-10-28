from enum import IntEnum, auto

class LEVEL_ID(IntEnum):
    LEVEL_MENU = 0
    LEVEL_TUTORIAL = 1
    LEVEL_QUEST = 2
    LEVEL_BOSS_ENTER = 3
    LEVEL_BOSS = 4
    END = 5


class level_manager:

    def __init__(self):
        self.cur_level = LEVEL_ID.LEVEL_MENU
        self.prev_level = LEVEL_ID.END
        self.level = None

    def level_change(self, level_id):
        self.cur_level = level_id

        if self.cur_level != self.prev_level:
            if self.level:
                self.level.release()

            if self.cur_level == LEVEL_ID.LEVEL_MENU:
                from Level_Menu import level_menu
                self.level = level_menu()

            elif self.cur_level == LEVEL_ID.LEVEL_TUTORIAL:
                from Level_Tutorial import level_tutorial
                self.level = level_tutorial()

            elif self.cur_level == LEVEL_ID.LEVEL_QUEST:
                from Level_Quest import level_quest
                self.level = level_quest()

            elif self.cur_level == LEVEL_ID.LEVEL_BOSS_ENTER:
                from Level_Boss_Enter import level_boss_enter
                self.level = level_boss_enter()

            elif self.cur_level == LEVEL_ID.LEVEL_BOSS:
                from Level_Boss import level_boss
                self.level = level_boss()

            self.level.initialize()
            self.prev_level = self.cur_level

    def update(self):
        if self.level:
            self.level.update()

    def late_update(self):
        if self.level:
            self.level.late_update()

    def render(self):
        if self.level:
            self.level.render()

    def release(self):
        if self.level:
            self.level.release()
            self.level = None