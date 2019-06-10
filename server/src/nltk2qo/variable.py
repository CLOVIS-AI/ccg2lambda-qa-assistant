from nltk2qo.entity import Entity


class Variable(Entity):

    def __init__(self, id: str):
        super().__init__(id)

    def __eq__(self, o: object) -> bool:
        return isinstance(
            o, Variable) and self.id is o.id and self.tags is o.tags

    def __str__(self) -> str:
        return "Variable{id=" + self.id + ", tags=[" + str(self.tags) + "]}"
