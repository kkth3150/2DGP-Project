class Animation:
    def __init__(self, image, frame_w, frame_h, frame_data, fps=8, loop=True):
        self.image = image
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.frame_data = frame_data  # 예: {'x':0,'y':0,'frame_count':3}
        self.fps = fps
        self.timer = 0
        self.frame_index = 0
        self.loop = loop
        self.is_finished = False  # 종료 플래그 추가

    def update(self, dt):
        if self.is_finished:
            return  # 끝났으면 더 이상 업데이트하지 않음

        self.timer += dt
        if self.timer > 1 / self.fps:
            self.timer = 0
            self.frame_index += 1
            if self.frame_index >= self.frame_data['frame_count']:
                if self.loop:
                    self.frame_index = 0
                else:
                    self.frame_index = self.frame_data['frame_count'] - 1
                    self.is_finished = True  # 애니 종료 플래그 ON

    def draw(self, x, y, scroll_x, scroll_y):
        sx = self.frame_data['x'] + self.frame_index * self.frame_w
        sy = self.frame_data['y']
        self.image.clip_draw(sx, sy, self.frame_w, self.frame_h, x - scroll_x, y - scroll_y)

class SkillAnimation:
    def __init__(self, image, frame_width, frame_height, frame_count, change_speed=0.05, loop=False):
        self.image = image
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_count = frame_count
        self.change_speed = change_speed
        self.loop = loop

        self.current_frame = 0
        self.acc_time = 0
        self.is_finished = False  # 애니 종료 플래그

    def update(self, dt):
        if self.is_finished:
            return

        self.acc_time += dt
        if self.acc_time >= self.change_speed:
            self.acc_time = 0
            self.current_frame += 1
            if self.current_frame >= self.frame_count:
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = self.frame_count - 1
                    self.is_finished = True

    def draw(self, x, y, scroll_x, scroll_y, flip=False, offset_x=0, offset_y=0):
        frame_x = self.current_frame * self.frame_width
        self.image.clip_draw(
            frame_x, 0,
            self.frame_width, self.frame_height,
            x - scroll_x + offset_x,
            y - scroll_y + offset_y
        )