from core.Database.Connection import Connection
from core.Database import Types as datatypes
from core.Entity.EntityBase import EntityBase

def getConnection(dbType, location, port=None, dbName=None, username=None, password=None, echo=False):
    return Connection(dbType, location, port, dbName, username, password, echo)
