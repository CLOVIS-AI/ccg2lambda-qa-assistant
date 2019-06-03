from typing import List, Union

from nltk2qo.entity import Entity
from nltk2qo.event import Event
from nltk2qo.variable import Variable
from qalogging import verbose, info, warning


class Sentence:

    def __init__(self):
        """
        Creates a Sentence object, with empty fields.
        """
        self.events: List[Event] = []
        self.__variables: List[Variable] = []
        self.main: Union[Variable, None] = None

    def add(self, name: str):
        """
        Adds an event or a variable to this Sentence.
        Based on the name, this will auto detect which one it is.
        If it already exists, it will not add it again.
        :param name: The name of the object to add.
        """
        if self.__is_event(name):
            self.add_event(name)
        else:
            self.add_variable(name)

    def add_variable(self, variable: str):
        """
        Adds a variable, if it doesn't already exist.
        :param variable: The name of the variable.
        """
        if variable not in [var.id for var in self.__variables]:
            self.__variables.append(Variable(variable))
            verbose(" › New variable [", variable, "]")

    def add_event(self, event: str):
        """
        Adds an event, if it doesn't already exist.
        :param event: The name of the event.
        """
        if event not in [event.id for event in self.events]:
            self.events.append(Event(event))
            verbose(" › New event [", event, "]")

    def add_tag(self, tag: str, entity: str):
        """
        Adds a tag to a specific entity.
        :param tag: The name of the tag
        :param entity: The entity on which the tag should be added
        """
        if tag == "QM":
            if self.main is None:
                self.main = self.__get_variable(entity)
                verbose(" › Main subject of the sentence: [", entity, "]")
            else:
                warning(
                    "Already found the main subject! It looks like there are 2 QM markers. Keeping the first one, "
                    "and ignoring this one on [", entity, "]")
        else:
            self.get_entity(entity).tags.append(tag)
            verbose(" › New tag [", tag, "] on [", entity, "]")

    def add_link(self, variable: str, event: str, link_name: str):
        """
        Adds a link between a variable and an event.
        :param variable: The name of the variable
        :param event: The name of the event
        :param link_name: The name of the link
        """
        e = self.get_event(event)
        e.variables.append((link_name, self.__get_variable(variable)))
        verbose(
            " › New link [",
            link_name,
            "] from [",
            event,
            "] to [",
            variable,
            "]")

    def get_entity(self, id_: str) -> Entity:
        """
        Find an entity (event or variable) from its name.
        :param id_: The name of the entity searched.
        :return: The entity, or None if it doesn't exist.
        """
        if Sentence.__is_event(id_):
            return self.get_event(id_)
        else:
            return self.__get_variable(id_)

    def get_event(self, id_: str) -> Event:
        """
        Find an event from its name.
        :param id_: The name of the event.
        :return: The event, or None if it doesn't exist.
        """
        return next((e for e in self.events if e.id == id_), None)

    def __get_variable(self, id_: str) -> Variable:
        """
        Find a variable from its name.
        :param id_: The name of the variable.
        :return: The variable, or None if it doesn't exist.
        """
        return next((v for v in self.__variables if v.id == id_), None)

    @staticmethod
    def __is_event(id_: str):
        if id_[0] == 'e':
            return True
        elif id_[0] == 'x':
            return False
        else:
            raise Exception(
                "Found [ " +
                id_ +
                "] which is neither an event (begins by e) nor a variable (begins by "
                "x)...")

    def pretty_print(self):
        """
        Graphically display this Sentence, to make it easier to see what's going on.
        """
        if self.main is not None:
            info(" question marker:", self.main.id, "[", *self.main.tags, "]")
        else:
            info(" question marker not found, this sentence is not a question!")

        info(" events:")
        for e in self.events:
            info(" - " + e.id + ":", "[", *e.tags, "]")
            for v in e.variables:
                info("   - " + v[0] + ":", v[1].id, "[", *v[1].tags, "]")
