import math

class CollisionManager:
    _instance = None

    @staticmethod
    def instance():
        if CollisionManager._instance is None:
            CollisionManager._instance = CollisionManager()
        return CollisionManager._instance

    def __init__(self):
        pass

    def collision_rect(self, dst_list, src_list):
        for dst in dst_list:
            for src in src_list:
                if self.check_rect_intersect(dst.get_col_rect(), src.get_col_rect()):
                    dst.hit(src)
                    src.hit(dst)

    def check_rect_intersect(self, a, b):
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b

        if ax1 > bx2: return False
        if ax2 < bx1: return False
        if ay1 > by2: return False
        if ay2 < by1: return False
        return True

    def collision_sphere(self, dst_list, src_list):
        for dst in dst_list:
            for src in src_list:
                if self.check_sphere(dst, src):
                    dst.hit(src)
                    src.hit(dst)

    def check_sphere(self, dst, src):
        dx = dst.x - src.x
        dy = dst.y - src.y
        dist = math.sqrt(dx * dx + dy * dy)
        radius = (dst.cx + src.cx) * 0.5
        return dist <= radius

    def collision_rect_ex(self, dst_list, src_list):
        for dst in dst_list:
            for src in src_list:
                px, py = self.check_rect_ex(dst, src)
                if px is not None:
                    if px > py:  # 상하 밀어내기
                        if dst.y < src.y:
                            dst.y -= py
                        else:
                            dst.y += py
                    else:        # 좌우 밀어내기
                        if dst.x < src.x:
                            dst.x -= px
                        else:
                            dst.x += px

                    dst.hit(src)
                    src.hit(dst)

    def check_rect_ex(self, dst, src):
        dx = abs(dst.x - src.x)
        dy = abs(dst.y - src.y)

        rx = (dst.cx + src.cx) * 0.5
        ry = (dst.cy + src.cy) * 0.5

        if rx > dx and ry > dy:
            px = rx - dx
            py = ry - dy
            return px, py

        return None, None

