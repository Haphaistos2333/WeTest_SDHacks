'''
WeTest - PermissionCoreTesting

10/17/2019
Tong created the file.
Tong created PermissionGroup interface.
'''

import Global
import WeTestObj


class PermissonGroup(WeTestObj.WeTestObj):

    __attributes = {'_version',
                    '_PermissonGroup__groupName',
                    '_PermissonGroup__permissions'}
    
    def __init__(self, groupName):
        super().__init__()
        self.__groupName = groupName
        self.__permissions = set()
        self.refreshPermission()

    def refreshPermission(self):
        '''
        Load the latest permission file. Permission file is named
          '#__groupName#.group' under Global.GROUP_DIR folder. Each line in
          the file represents a permission node.
        '''
        pass  # Implement this function
    
    def getPermissions(self) -> {str}:
        return self.__permissions.copy()

    def pickleSave(self):
        filename = self.__groupName + Global.GROUP_EXT
        super().pickleSave(Global.GROUP_DIR, filename)