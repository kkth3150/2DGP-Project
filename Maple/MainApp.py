from pico2d import *
from Level_Manager import level_manager, LEVEL_ID
import time

class MainApp:
    def __init__(self):
        self.running = True
        self.level_manager = level_manager()

    def initialize(self):
        self.level_manager.level_change(LEVEL_ID.LEVEL_MENU)
        pass

    def update(self, dt):
        self.level_manager.update(dt)
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

TARGET_FPS = 60
TARGET_DT = 1.0 / TARGET_FPS
last_time = time.time()

mainapp = MainApp()
mainapp.initialize()

while mainapp.running:
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    mainapp.update(dt)
    mainapp.late_update()
    mainapp.render()

    elapsed = time.time() - current_time
    sleep_time = TARGET_DT - elapsed
    if sleep_time > 0:
        delay(sleep_time * 1000)  # delay는 ms 단위

mainapp.release()
close_canvas()