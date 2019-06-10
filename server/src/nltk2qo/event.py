from typing import List, Tuple

from nltk2qo.entity import Entity
from nltk2qo.variable import Variable


class Event(Entity):

    def __init__(self, id_: str):
        super().__init__(id_)
        self.variables: List[Tuple[str, Variable]] = []

    def __str__(self) -> str:
        return "Event{id=" + self.id + \
            ", tags=[" + str(self.tags) + "], variables=[" + str(self.variables) + "]}"
