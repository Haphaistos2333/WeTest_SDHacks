"""
Author: Litian Liang, Tong Liu
Oct 26 10:57 AM

Documentation:
class AnyObject(WeTestObj): to create more classes

    1: __init__(dummy = False)
        use super().__init__() to construct any object
        use super().__init__(True) to create dummy object

    2: AnyObject must implement dum() method which calls
        the dummy=True constructor to create a object with all
        field variables. Give them any values, this method is
        used for database type checking!

    3: AnyObject().mangoSave() to save this object

    4: Use AnyObject.mangoLoad(serial: int) to load a object back
"""

# project module
import Global
import WeTestExceptions
# import WeTestExceptions

# database module
from DataBase import DataBase

class WeTestObj:
    '''
    Base class for WeTest objects.
    '''
    mangodb = DataBase()


    def __init__(self, dummy=False):
        """ create a new wetest obj """

        # version var
        self._version = Global.CURR_VERSION
        if not dummy:
            # database var
            self.serial = Global.NEXT_SERIAL
            Global.NEXT_SERIAL += 1
        else:
            self.serial = -1
    
    def checkVersion(self):
        if self._version != Global.CURR_VERSION:
            missedAttributes = self.__attributes - set(self.__dict__.keys())
            raise WeTestExceptions.UpdateNeededException(missedAttributes)
    
    def mangoUpdate(self):
        return self.mangodb.update(self)
    
    def mangoSave(self):
        return self.mangodb.save(self)

    @classmethod
    def mangoLoad(cls, serial):
        """ load obj from database """
        return cls.mangodb.load(serial)