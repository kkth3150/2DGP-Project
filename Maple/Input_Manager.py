from pico2d import *

class Input_manager:
    _instance = None

    @staticmethod
    def instance():
        if Input_manager._instance is None:
            Input_manager._instance = Input_manager()
        return Input_manager._instance

    def __init__(self):
        self.key_down = {}
        self.key_pressed = {}
        self.key_up = {}
        self.mouse_down = {}
        self.mouse_pressed = {}
        self.mouse_up = {}

        self.mouse_x = 0
        self.mouse_y = 0

    def update(self):
        events = get_events()
        self.key_down.clear()
        self.key_up.clear()
        self.mouse_down.clear()
        self.mouse_up.clear()

        for e in events:
            if e.type == SDL_KEYDOWN:
                self.key_down[e.key] = True
                self.key_pressed[e.key] = True
            elif e.type == SDL_KEYUP:
                self.key_up[e.key] = True
                if e.key in self.key_pressed:
                    del self.key_pressed[e.key]

            elif e.type == SDL_MOUSEBUTTONDOWN:
                self.mouse_down[e.button] = True
                self.mouse_pressed[e.button] = True
            elif e.type == SDL_MOUSEBUTTONUP:
                self.mouse_up[e.button] = True
                if e.button in self.mouse_pressed:
                    del self.mouse_pressed[e.button]

            elif e.type == SDL_MOUSEMOTION:
                self.mouse_x, self.mouse_y = e.x, get_canvas_height() - e.y - 1

            elif e.type == SDL_QUIT:
                self.key_pressed.clear()
                self.mouse_pressed.clear()

    # --- 키 관련 ---
    def Key_Down(self, key): return self.key_down.get(key, False)
    def Key_Up(self, key): return self.key_up.get(key, False)
    def Key_Pressing(self, key): return self.key_pressed.get(key, False)

    # --- 마우스 관련 ---
    def Mouse_Down(self, button): return self.mouse_down.get(button, False)
    def Mouse_Up(self, button): return self.mouse_up.get(button, False)
    def Mouse_Pressing(self, button): return self.mouse_pressed.get(button, False)
    def Mouse_Pos(self): return self.mouse_x, self.mouse_y