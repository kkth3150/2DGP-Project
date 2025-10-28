from pico2d import *
from LevelManager.Level_Manager import level_manager, LEVEL_ID

class MainApp:
    def __init__(self):
        self.running = True
        self.level_manager = level_manager()

    def initialize(self):
        self.level_manager.level_change(LEVEL_ID.LEVEL_MENU)
        pass

    def update(self):
        self.level_manager.update()
        pass

    def late_update(self):
        self.level_manager.late_update()
        pass

    def render(self):
        clear_canvas()
        self.level_manager.render()
        update_canvas()

    def release(self):
        self.level_manager.release()
        pass

open_canvas()

mainapp = MainApp()
mainapp.initialize()

while mainapp.running:
    mainapp.update()
    mainapp.late_update()
    mainapp.render()
    delay(0.01)

mainapp.release()
close_canvas()