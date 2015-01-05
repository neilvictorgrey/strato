from core.Database.Connection import Connection
from core.Database import Types as datatypes
from core.Entity.EntityBase import EntityBase

def getConnection(type, location, port=None, dbName=None, username=None, password=None, echo=False):
    return Connection(type, location, port=None, dbName=None, username=None, password=None, echo=False)
