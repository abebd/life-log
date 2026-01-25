import logging

from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class Storage(ABC):
    @property
    def type(self) -> str:
        raise NotImplementedError("Subclasses must implemnet the 'type' property")

    @abstractmethod
    def add_entry(self, body, timestamp):
        pass

    @abstractmethod
    def update_entry(self, old_entry, new_entry):
        pass

    @abstractmethod
    def open_entry(self, body, timestamp):
        pass

    @abstractmethod
    def get_entries(self) -> list:
        pass
