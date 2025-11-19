from enum import IntEnum, auto
from Collision_Manager import CollisionManager

OBJ_DEAD = 1
OBJ_ALIVE = 0

class OBJ(IntEnum):
    BACKGROUND = 0
    NPC = 1
    MONSTER = 2
    BOSS = 3
    PLAYER = 4
    EFFECT = 5
    DAMAGE = 6
    PLAYER_SKILLBOX = 7
    MONSTER_SKILLBOX = 8
    UI = 9
    END = 10


class ObjectManager:
    _instance = None

    @staticmethod
    def instance():
        if ObjectManager._instance is None:
            ObjectManager._instance = ObjectManager()
        return ObjectManager._instance

    def __init__(self):
        if ObjectManager._instance is not None:
            raise Exception("Use ObjectManager.instance() instead of direct instantiation.")
        self.objects = [[] for _ in range(OBJ.END)]

    def add_object(self, obj, obj_type: OBJ):
        self.objects[obj_type].append(obj)

    def remove_object(self, obj, obj_type: OBJ):
        if obj in self.objects[obj_type]:
            self.objects[obj_type].remove(obj)

    def get_objects(self, obj_type: OBJ):
        return self.objects[obj_type]

    def update(self, dt):
        collision_mgr = CollisionManager.instance()
        player_skillboxes = self.objects[OBJ.PLAYER_SKILLBOX]
        monsters = self.objects[OBJ.MONSTER] + self.objects[OBJ.BOSS]  # 보스도 포함 가능
        collision_mgr.collision_rect(player_skillboxes, monsters)

        for obj_list in self.objects:
            dead = []
            for obj in obj_list:
                if obj.update(dt) == OBJ_DEAD:
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
                continue
            for obj in obj_list:
                if hasattr(obj, "release"):
                    obj.release()
            obj_list.clear()