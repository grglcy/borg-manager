from . import DBObject


class Label(DBObject):
    def __init__(self, label: str, primary_key=None):
        super(Label, self).__init__(primary_key)
        self.label = label
