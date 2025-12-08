class GameObject:
    def __init__(self, x=0, y=0, size=0):
        self.x = x
        self.y = y
        self.size = size
        self.image_size = size
        self.is_dead = False
        self.col_w = x
        self.col_h = y
        self.max_hp = 0


    def update(self, dt):
        pass

    def late_update(self):
        pass

    def render(self):
        pass

    def release(self):
        pass

    # 기본 충돌 처리
    def hit(self, other):
        pass

    def get_col_rect(self):
        # 중심 기준 충돌 박스 반환
        left = self.x - self.col_w // 2
        right = self.x + self.col_w // 2
        bottom = self.y - self.col_h // 2
        top = self.y + self.col_h // 2
        return left, right, bottom, top

    def set_dead(self):
        self.is_dead = True