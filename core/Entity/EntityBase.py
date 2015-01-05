from strato.core.Database.Types import Column, String, Integer
from strato.core.Database.StratoBase import StratoBase

class EntityBase(StratoBase):
    __abstract__ = True

    def __init__(self, **kwargs):
        super(EntityBase, self).__init__(**kwargs)
    
    @classmethod
    def register(cls, connection):
        cls.addAttribute('id', Integer, primary_key=True)
        cls.addAttribute('version', Integer)
        super(EntityBase, cls).register(connection)
