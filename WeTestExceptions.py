'''
WeTest - PermissionCoreTesting

10/17/2019
Tong created the file.
Tong added UpdateNeededException.
Tong added ActionNoPermissionError.
'''


class UpdateNeededException(Exception):
    '''
    WeTest Exception: raise if version not matched
    '''

    def __init__(self, missedAttributes: {str}, what='UpdateNeeded'):
        super().__init__(what)
        self.__missedAttributes = missedAttributes
    
    def getMissedAttributes(self) -> {str}:
        return self.__missedAttributes

    
class ActionNoPermissionError(Exception):
    '''
    WeTest Exception: raise if unauthorised user tried an action.
    '''

    def __init__(self, user, action, what='Action No Permission'):
        super().__init__(what)
        self.__user = user
        self.__action = action

class SerialNumberNotFound(Exception):
    pass