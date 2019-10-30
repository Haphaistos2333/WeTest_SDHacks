'''
WeTest - User
'''

# WeTest Components
import Global
import WeTestObj

# extern libs
import pickle

# Enabling flask user login
from flask_login import UserMixin

# Private class: Crucial Username Password relation, DO NOT MODIFY
class U_P_db:
    def __init__(self, filelocation):
        self.usr_pswd = None
        self.filelocation = filelocation
        with open(filelocation, 'rb') as u_p:
            self.usr_pswd = pickle.load(u_p);

    # queries
    def hasUser(self, key: (str, str)):
        return key in self.usr_pswd

    def hasUsername(self, username: str) -> bool:
        for usr, pswd in self.usr_pswd:
            if usr == username:
                return True
        return False

    # getter methods
    def getSerial(self, key: (str, str)):
        """ when have both usrname and pswd """
        return self.usr_pswd[key]

    def getSerialByName(self, key):
        """ when only have username"""
        for (usr, _), serial in self.usr_pswd.items():
            if usr == key:
                return serial
        return None

    # mutators
    def addUser(self, usr, pswd, serial):
        self.usr_pswd[(usr, pswd)] = serial
        with open(self.filelocation, 'wb') as datafile:
            pickle.dump(self.usr_pswd, datafile)



# User class for login
class User(WeTestObj.WeTestObj, UserMixin):
    # load all user and password
    # as { (username, password) : serial_number }
    usr_pswd = U_P_db("usr_pswd.pkl")

    def __init__(self,
                 username: str,
                 pswd: str,
                 group=set(),
                 dummy=False):
        super().__init__(dummy)
        # necessary attributes, do not modify
        self.__username = username
        self.__pswd = pswd
        self.__group = group
        self.asmtList = []

        # for flask-login, now set default equal to username
        self.id = self.__username

    def joinAsmt(self, asmtSerial):
        self.asmtList.append(asmtSerial)

    @classmethod
    def dum(cls):
        """ for database type checking """
        dumobj = cls("", "", dummy=True)
        return dumobj

    def getPermissions(self) -> {str}:
        res = set()
        for g in self.__group:
            res.update(g.getPermissions())
        return res

    def matchPassword(self, pswdIn):
        ''' compare passwordIn and __pswd '''
        return pswdIn == self.__pswd

    @classmethod
    def fromLogin(cls, username, password):
        if cls.usr_pswd.hasUser((username, password)):
            serial = cls.usr_pswd.getSerial((username, password))
            print("serial:", serial)
            return cls.mangoLoad(serial)
        else:
            return None

    @classmethod
    def newUser(cls, username, password):
        newuser = User(username, password)
        newuser.serial = Global.NEXT_SERIAL
        newuser.mangoSave()
        cls.usr_pswd.addUser(username, password, newuser.serial)
        return newuser

    # flask-login method
    def get_id(self):
        return self.id

    # flask-login method
    def is_authenticated(self):
        ''' implement in future '''
        return True