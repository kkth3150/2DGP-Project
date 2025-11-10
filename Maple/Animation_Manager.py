class Animation:
    def __init__(self, image, frame_w, frame_h, frame_data, fps=8):
        self.image = image
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.frame_data = frame_data  # 예: [(x, y, frame_count)]
        self.fps = fps
        self.timer = 0
        self.frame_index = 0

    def update(self, dt):
        self.timer += dt
        if self.timer > 1 / self.fps:
            self.timer = 0
            self.frame_index = (self.frame_index + 1) % self.frame_data['frame_count']

    def draw(self, x, y, scroll_x, scroll_y):
        sx = self.frame_data['x'] + self.frame_index * self.frame_w
        sy = self.frame_data['y']
        self.image.clip_draw(sx, sy, self.frame_w, self.frame_h, x - scroll_x, y - scroll_y)