from pico2d import *

class Line:
    def __init__(self, x1, y1, x2, y2, thickness=5):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.thickness = thickness

    def equation_y(self, x):
        if self.x2 - self.x1 == 0:
            return self.y1
        return ((self.y2 - self.y1) / (self.x2 - self.x1)) * (x - self.x1) + self.y1

    def render(self, scroll_x=0, scroll_y=0):
        left = min(self.x1, self.x2) - scroll_x
        right = max(self.x1, self.x2) - scroll_x
        top = max(self.y1, self.y2) - scroll_y + self.thickness / 2
        bottom = min(self.y1, self.y2) - scroll_y - self.thickness / 2
        draw_rectangle(left, bottom, right, top)


class LineManager:
    _instance = None

    @staticmethod
    def instance():
        if LineManager._instance is None:
            LineManager._instance = LineManager()
        return LineManager._instance

    def __init__(self):
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

    def collision_line(self, x, y, move_y):
        """
        X 좌표에서 y 충돌 판정
        :param x: 플레이어 X
        :param y: 플레이어 현재 Y
        :param move_y: 이동량
        :return: 충돌한 Y 좌표, 충돌 여부
        """
        if not self.lines:
            return y, False

        min_delta = float('inf')
        collided_y = y
        for line in self.lines:
            # 플레이어 X가 라인 범위 안에 있는지 확인
            if line.x1 <= x <= line.x2 or line.x2 <= x <= line.x1:
                line_y = line.equation_y(x)
                delta = line_y - y
                # 아래 방향으로만 충돌 체크
                if -move_y <= delta < min_delta:
                    min_delta = delta
                    collided_y = line_y

        return collided_y, min_delta != float('inf')

    def render(self, scroll_x=0, scroll_y=0):
        for line in self.lines:
            line.render(scroll_x, scroll_y)