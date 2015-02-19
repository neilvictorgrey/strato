from strato.core.Database.Types import Integer, Boolean, DateTime
from strato.core.Database.StratoBase import StratoBase

class EntityBase(StratoBase):
    __abstract__ = True
    __active = False
    __connection = None

    def __init__(self, **kwargs):
        
        self.__active = False
        self.__connection = None
        super(EntityBase, self).__init__(**kwargs)
    
    @classmethod
    def register(cls, connection):
        
        cls.addParameter('id', Integer, primary_key=True)
        cls.addParameter('version', Integer)
        cls.addParameter('active', Boolean)
        cls.addParameter('lastEdited', DateTime)
        cls.addParameter('lastEditedBy', Integer)
        super(EntityBase, cls).register(connection)
    
    @classmethod
    def activate(cls, connection):
        
        if not cls.__active:
            cls.__connection = connection
            cls.prepare(cls.__connection.getEngine())
            #cls.__connection.addClass(cls)
            cls.__active = True
    
    @classmethod
    def getConnection(cls):
        return cls.__connection
    
    def getInstance(self):
        
        instance = None
        connection = self.getConnection()
        if connection:
            session = connection.getSession()
            entityType = type(self)
            instance = session.query(entityType).filter(entityType.id==self.id).one()
        return instance
    
    def flushSession(self):
        
        connection = self.getConnection()
        if connection:
            session = connection.getSession()
            session.flush()
    
    @classmethod
    def create(self, **kwargs):
        
        instance = None
        connection = self.getConnection()
        if connection:
            session = connection.getSession()
            instance = self(version=1, active=True, **kwargs)
            session.add(instance)
            session.commit()
        return instance

    def update(self, **kwargs):
        
        instance = self.getInstance()
        if instance:
            for k in kwargs.keys():
                setattr(instance, k, kwargs[k])
            self.flushSession()

        return True
    
    def retire(self):
        
        return True
