from abc import ABC


class DBObject(ABC):
    def __init__(self, primary_key=None):
        self.__primary_key = primary_key

    @property
    def primary_key(self):
        if self.__primary_key is None:
            raise ValueError("Primary key is None")
        else:
            return self.__primary_key
