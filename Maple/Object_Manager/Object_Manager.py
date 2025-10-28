from enum import IntEnum, auto

class OBJ(IntEnum):
    MONSTER = 0
    BOSS = 1
    PLAYER = 2
    EFFECT = 3
    END = 4

class ObjectManager:
    def __init__(self):
        # OBJ_END 크기만큼 리스트 준비
        self.objects = [[] for _ in range(OBJ.END)]

    def add_object(self, obj, obj_type: OBJ):
        self.objects[obj_type].append(obj)

    def remove_object(self, obj, obj_type: OBJ):
        if obj in self.objects[obj_type]:
            self.objects[obj_type].remove(obj)

    def update(self):
        for obj_list in self.objects:
            dead = []
            for obj in obj_list:
                if obj.update() == 1:  # dead flag
                    dead.append(obj)
            for obj in dead:
                if hasattr(obj, "release"):
                    obj.release()
                obj_list.remove(obj)

    def late_update(self):
        for obj_list in self.objects:
            for obj in obj_list:
                if hasattr(obj, "late_update"):
                    obj.late_update()

    def render(self):
        for obj_list in self.objects:
            for obj in obj_list:
                if hasattr(obj, "render"):
                    obj.render()
