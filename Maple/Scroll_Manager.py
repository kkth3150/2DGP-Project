class ScrollManager:
    _instance = None

    @staticmethod
    def instance():
        if ScrollManager._instance is None:
            ScrollManager._instance = ScrollManager()
        return ScrollManager._instance

    def __init__(self):
        # 현재 스크롤 위치
        self.scroll_x = 0
        self.scroll_y = 0

        # 화면 크기
        self.win_width = 800
        self.win_height = 600

        # 맵 크기 (실제 맵의 픽셀)
        self.map_width = 1733  # 예시
        self.map_height = 1464

        # 스크롤 락
        self.lock_x = False
        self.lock_y = False

    def set_map_size(self, w, h):
        self.map_width = w
        self.map_height = h

    def set_scroll_x(self, dx):
        if not self.lock_x:
            self.scroll_x += dx
            self.lock_scroll()

    def set_scroll_y(self, dy):
        if not self.lock_y:
            self.scroll_y += dy
            self.lock_scroll()

    def lock_scroll(self):
        # 스크롤을 맵 범위 안으로 제한
        self.scroll_x = max(0, min(self.scroll_x, self.map_width - self.win_width))
        self.scroll_y = max(0, min(self.scroll_y, self.map_height - self.win_height))

    def get_scroll(self):
        return self.scroll_x, self.scroll_y