from strato import EntityBase, datatypes, getConnection

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
        
        cls.addParameter('username', datatypes.String(100))
        cls.addParameter('fullname', datatypes.String(100))
        super(User, cls).register(connection)


def createUser():
    
    #################
    # TESTING ONLY  #
    StratoConnection = getConnection('sqlite',':memory:', echo=True)
    User.register(StratoConnection)
    User.activate(StratoConnection)
    # TESTING ONLY  #
    #################
    
    user = User.create(username='neil', fullname='Neil Grey')
    user.update(fullname='John Grey')
    print user.fullname
    