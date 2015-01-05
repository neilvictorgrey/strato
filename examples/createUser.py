from strato import EntityBase, datatypes, getConnection

from sqlalchemy.orm import sessionmaker

class User(EntityBase):

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        
    def __repr__(self):
        return "User({id}, {login}, {name})".format(
                id=self.id, 
                login=self.username, 
                name=self.fullname
            )

    @classmethod
    def register(cls, connection):
        cls.addAttribute('username', datatypes.String(100))
        cls.addAttribute('fullname', datatypes.String(100))
        super(User, cls).register(connection)

StratoConnection = getConnection('sqlite',':memory:', echo=True)
StratoEngine = StratoConnection.getEngine()

User.register(StratoConnection)
User.prepare(StratoEngine)

session = sessionmaker(bind=StratoEngine)()
user = User(username='neil', fullname='Neil Grey')
session.add(user)
session.commit()
print user
