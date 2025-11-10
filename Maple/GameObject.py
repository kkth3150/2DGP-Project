class GameObject:
    def __init__(self, x=0, y=0, size=0):
        self.x = x
        self.y = y
        self.size = size
        self.image_size = size
        self.is_dead = False

    def update(self, dt):
        pass

    def late_update(self):
        pass

    def render(self):
        pass

    def release(self):
        pass