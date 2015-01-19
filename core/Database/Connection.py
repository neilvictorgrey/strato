import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

class Connection(object):
    
    def __init__(self, dbType, location, port=None, dbName=None, username=None, password=None, echo=False):
        
        self._dbType = dbType
        self._location = location
        self._port = port
        self._dbName = dbName
        self._username = username
        self._password = password
        self._echo = echo

        self.__createEngine()
        
        self._metadata = sqlalchemy.MetaData(bind=self.getEngine())
        self.__session = None
    
    def __createEngine(self):
        
        assert self._dbType in self.getSupportedProtocols().keys()
        
        if self._dbType == 'sqlite':
            dbAddress = '{protocol}{location}'
        else:
            dbAddress = '{protocol}{username}:{password}@{location}'
            if self._port:
                dbAddress += ':{port}'
            if self._dbName:
                dbAddress += '/{dbName}'
        
        uri = dbAddress.format(
            protocol = self.getSupportedProtocols()[self._dbType],
            username = self._username,
            password = self._password,
            location = self._location,
            port = self._port,
            dbName = self._dbName,
        )
        
        self.__engine = create_engine(uri, echo=self._echo)
    
    @staticmethod
    def getSupportedProtocols():
        
        protocols = {
            'postgresql':'postgresql+psycopg2://',
            'sqlite':'sqlite:///',
        }
        return protocols
    
    def getEngine(self):

        return self.__engine
    
    def getSession(self):
        
        if not self.__session:
            self.__session = scoped_session(sessionmaker(self.__engine))
        return self.__session
    
    def close(self):
        
        if self.__session:
            self.__session.close()
            self.__session = None
        
    