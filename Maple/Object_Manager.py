from enum import IntEnum, auto

OBJ_DEAD = 1
OBJ_ALIVE = 0

class OBJ(IntEnum):
    MONSTER = 0
    BOSS = 1
    PLAYER = 2
    EFFECT = 3
    UI = 4
    END = 5

class ObjectManager:
    def __init__(self):
        self.objects = [[] for _ in range(OBJ.END)]

    def add_object(self, obj, obj_type: OBJ):
        self.objects[obj_type].append(obj)

    def remove_object(self, obj, obj_type: OBJ):
        if obj in self.objects[obj_type]:
            self.objects[obj_type].remove(obj)

    def get_objects(self, obj_type: OBJ):
        return self.objects[obj_type]

    def update(self,dt):
        for obj_list in self.objects:
            dead = []
            for obj in obj_list:
                if obj.update(dt) == OBJ_DEAD:  # dead flag
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

    def release_all_except(self, keep_types):
        for obj_type, obj_list in enumerate(self.objects):
            if OBJ(obj_type) in keep_types:
                continue  # 유지할 타입은 건너뜀
            for obj in obj_list:
                if hasattr(obj, "release"):
                    obj.release()
            obj_list.clear()