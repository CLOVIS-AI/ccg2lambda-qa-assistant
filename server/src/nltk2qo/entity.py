from typing import List


class Entity:

    def __init__(self, id_: str):
        self.tags: List[str] = []
        self.id: str = id_
