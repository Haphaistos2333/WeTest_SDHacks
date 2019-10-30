import pymongo
import Global


def type_as_str(x):
    return str(type(x))[8:-2]


class DataBase:

    def __init__(self):
        """ connect to server, initialize max serial number """
        self.db = pymongo.MongoClient(host=Global.MONGO_HOST,
                                      port=Global.MONGO_PORT)['WeTest']
                                      
        # Get max using pipeline
        pipelineRes = list(self.db.WeTestObj.aggregate([
            {'$group':{
                '_id':'res',
                'res':{'$max':'$serial'}
                }}
            ]))
        if pipelineRes:
            maxSerial = pipelineRes[0]['res']
            Global.NEXT_SERIAL = max(maxSerial + 1, Global.NEXT_SERIAL)

    def load(self, serial: int):
        """ returns a WeTest based object with type """
        
        import User
        import Assignment
        try:
            objType = self.db['WeTestObj'].find_one({'serial': serial})['type']
        except:
            return None
        
        
        res = eval(objType + '.dum()')
        
        val = self.db[objType].find_one({'serial': str(serial)})
        
        # _id hashed id given by mongoDB
        res.__dict__ = dict([(i, eval(val[i])) for i in val if i != '_id']) 
        
        return res
    
    def update(self, obj):
        assert type_as_str(obj) == self.db['WeTestObj'].find_one({'serial': obj.serial})['type']
        objType = type_as_str(obj)
        self.db[objType].find_one_and_delete({'serial': str(obj.serial)})
        self.save(obj)
    
    def save(self, obj):
        """ saves a wetest object, returns a serial number """
        
        objType = type_as_str(obj)
        
        entry = {
            'serial': obj.serial,
            'type': objType
        }
        
        self.db['WeTestObj'].insert_one(entry)  # Serial->Type
        
        content = dict([(i, repr(obj.__dict__[i])) for i in obj.__dict__])

        return self.db[objType].insert_one(content)


if __name__ == '__main__':
    db = DataBase()
    print(db.load(21))
#     from WeTestObj import WeTestObj
#     
#     class Dummy1(WeTestObj):
# 
#         def __init__(self, dummy=False):
#             if not dummy:
#                 super().__init__()
#                 self.int = 1
#                 self.float = 2.
#                 self.tuple = (1, 2)
#                 self.set = {'str1', 'str2'}
#                 self.str = 'str'
# 
#         @staticmethod
#         def dum():
#             return Dummy1(dummy=True)
#             
#     class Dummy2(WeTestObj):
# 
#         def __init__(self, dummy=False):
#             if not dummy:
#                 super().__init__()
#                 self.int = 2
#                 self.float = 2.
#                 self.tuple = (1, 2)
#                 self.set = {'str1', 'str2'}
#                 self.str = 'str'
#         
#         @staticmethod
#         def dum():
#             return Dummy2(dummy=True)
#     
#     class DummyN(WeTestObj):
# 
#         def __init__(self, n, dummy=False):
#             if not dummy:
#                 super().__init__()
#                 self.int = n
#                 self.float = 2.
#                 self.tuple = (1, 2)
#                 self.set = {'str1', 'str2'}
#                 self.str = 'str'
# 
#         @staticmethod
#         def dum():
#             return DummyN(0, dummy=True)
#             
#     db = DataBase()
#     
#     # Testing Save
#     
#     o1 = Dummy1()
#     print("###", db.save(o1))
#     print(o1.__dict__)
#     
#     o2 = Dummy2()
#     db.save(o2)
#     print(o2.__dict__)
#     
#     o3 = DummyN(5)
#     db.save(o3)
#     print(o3.__dict__)
#     
#     o4 = Dummy2()
#     db.save(o4)
#     print(o4.__dict__)
#     
#     print()
#     
#     # Testing load
#     ol1 = db.load(103)
#     print(ol1)
#     print(ol1.__dict__)
#     
#     ol2 = db.load(102)
#     print(ol2)
#     print(ol2.__dict__)
