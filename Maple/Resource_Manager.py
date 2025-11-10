import os
from pico2d import load_image

class ResourceManager:
    _instance = None

    @staticmethod
    def instance():
        if ResourceManager._instance is None:
            ResourceManager._instance = ResourceManager()
        return ResourceManager._instance

    def __init__(self):
        if ResourceManager._instance is not None:
            raise Exception("Use ResourceManager.instance() instead of direct instantiation.")
        self._resources = {}

    def load(self, key, path):
        if key not in self._resources:
            self._resources[key] = load_image(path)

    def get(self, key):
        return self._resources.get(key)

    def release_all(self):
        self._resources.clear()