import inspect

from sqlalchemy.ext.declarative import DeferredReflection, declarative_base, declared_attr

from Types import Table, Column, Integer

Base = declarative_base(cls=DeferredReflection)
class StratoBase(Base):
    __abstract__ = True
    
    @declared_attr
    def __tablename__(cls):
        # /todo: make this way more bulletproof than "classes[1]"
        classes = inspect.getmro(cls)
        tablename = "{child}_{parent}".format(
                child = cls.__name__.lower(), 
                parent = classes[1].__name__.lower().replace('base',''),
            )
        return tablename
    
    @classmethod
    def addAttribute(cls, name, type, **kwargs):
        setattr(cls, name, Column(name, type, **kwargs))
        
    # /todo: addAttributes method
    
    @classmethod
    def getColumns(cls):
        return [x[1] for x in inspect.getmembers(cls) if type(x[1])==Column]

    @classmethod
    def register(cls, connection):
        table = Table(cls.__tablename__, connection._metadata, *cls.getColumns(), extend_existing=True)
        connection._metadata.create_all(connection.getEngine())
        