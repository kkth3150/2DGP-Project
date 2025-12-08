from pico2d import *
from Level_Manager import level_manager, LEVEL_ID
import time
from Input_Manager import Input_manager

class MainApp:
    def __init__(self):
        self.running = True
        self.level_manager = level_manager.instance()

    def initialize(self):
        self.level_manager.level_change(LEVEL_ID.LEVEL_TUTORIAL)

    def update(self, dt):
        self.level_manager.update(dt)

    def late_update(self):
        self.level_manager.late_update()

    def render(self):
        clear_canvas()
        self.level_manager.render()
        update_canvas()

    def release(self):
        self.level_manager.release()

open_canvas()

TARGET_FPS = 60
TARGET_DT = 1.0 / TARGET_FPS
last_time = time.time()

mainapp = MainApp()
mainapp.initialize()
input_mgr = Input_manager.instance()


while mainapp.running:
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    input_mgr.update()
    mainapp.update(dt)
    mainapp.late_update()
    mainapp.render()
    elapsed = time.time() - current_time
    sleep_time = TARGET_DT - elapsed

    if sleep_time > 0:
        time.sleep(sleep_time)

mainapp.release()
close_canvas()