import Global
import WeTestObj


# Assignment class for assigner, inside User class
class Assignment(WeTestObj.WeTestObj):
     
    def __init__(self, assigner: str, asmtName: str, dummy=False):
        super().__init__(dummy)
        
        self.asmtName = asmtName

        # the id of the assigner
        self.__assigner = assigner 
        
        # {func_name: [(return_value, input_args), ]}
        self._functions_sample = {}
        
        # {id: studentFileSerial}
        self.__studentFile = {}
        
        # {id: {func_name: [testcase1Serial, testcase2Serial, testcase3Serial]}}   3 testcases for each function
        self.__testcase = {}

    @classmethod
    def dum(cls):
        return Assignment('', '', dummy = True)




        
#     def __repr__(self):
#         return str(self.__testcase)
        
    def upload(self, id, py: str) -> (['TestcaseSerial'],['TestcaseSerial']):
        """ upload the studentFile, return passedTest and failedTest """
        stdFile = StudentFile(id, py)
        stdFile.mangoSave()
        StudentFile.checkTest(stdFile, self)
        self.__studentFile.setdefault(id, stdFile.serial)
        stdFile.mangoUpdate()
        return (stdFile.getPassedTests(), stdFile.getFailedTests())
    
    
    def deletefile(self, id) -> bool:
        """ delete the studentFile, return whether it's succeed """
        if id in self.__studentFile:
            del self.__studentFile[id]
            return True
        return False
    
    
    def uploadTest(self, id,
                   func_name: str, 
                   return_value, 
                   *input_args):
        """ upload the testcase """
        self.__testcase.setdefault(id, {})
        self.__testcase[id].setdefault(func_name, [])
        tc = Testcase(func_name, return_value, *input_args)
        tc.mangoSave()
        self.__testcase[id][func_name].append(tc.serial)
        self._updateStudent(tc)
    
    
    def deleteTest(self, id,
                   func_name: str, 
                   return_value, 
                   *input_args) -> bool:
        """ delete a testcase, return whether succeed"""
        if id in self.__testcase:
            if func_name in self.__testcase[id]:
                for testcaseSerial in self.__testcase[id][func_name]:
                    if return_value == WeTestObj.WeTestObj.mangoLoad(testcaseSerial).getReturn() and\
                        input_args == WeTestObj.WeTestObj.mangoLoad(testcaseSerial).getInputs():
                        self.__testcase[id][func_name].remove(testcaseSerial)
                        self._deleteTest(WeTestObj.WeTestObj.mangoLoad(testcaseSerial))
                        return True
        return False
        
        
    def addSampleTestcase(self,
                          func_name: str,
                          return_value: str,
                          *input_args):
        """ add samples, samples are also testcases """
        self._functions_sample.setdefault(func_name, [])
        self._functions_sample[func_name].append((return_value, input_args))
        self.__testcase.setdefault(self.__assigner, {})
        self.__testcase[self.__assigner].setdefault(func_name, [])
        tc = Testcase(func_name, return_value, *input_args)
        tc.mangoSave()
        self.__testcase[self.__assigner][func_name].append(tc.serial)
        self._updateStudent(tc)
      
      
        
    # helper method   
    def _updateStudent(self, testcase):
        for stdFileSerial in self.getStdFile().values():
            stdFile = WeTestObj.WeTestObj.mangoLoad(stdFileSerial)
            Test = stdFile.getModule()
            for func_name in self.getFunctions():
                if func_name == testcase.getName():
                    if testcase.passThisTest(func_name, Test):
                        stdFile._passedTest.append(testcase.serial)
                    else:
                        stdFile._failedTest.append(testcase.serial)
                        
    def _deleteTest(self, testcase):
        for stdFileSerial in self.getStdFile().values():
            stdFile = WeTestObj.WeTestObj.mangoLoad(stdFileSerial)
            if testcase.serial in stdFile.getPassedTests():
                stdFile._passedTest.remove(WeTestObj.WeTestObj.mangoLoad(testcase.serial))
            elif testcase.serial in stdFile.getFailedTests():
                stdFile._failedTest.remove(WeTestObj.WeTestObj.mangoLoad(testcase.serial))
                    
    
    
    # getter methods
    def getTestcases(self):
        return self.__testcase
    
    def getStdFile(self):
        return self.__studentFile
    
    def getLenTest(self, id, func_name):
        """ get how many testcases have been uploaded for the function, 3 is required """
        return len(self.__testcase[id][func_name])
       
    def getFunctions(self):
        return self._functions_sample
    
    def getResult(self, id) -> (['Testcase'],['Testcase']):
        if id in self.__studentFile:
            return (self.mangoLoad(self.__studentFile[id]).getPassedTests(), self.mangoLoad(self.__studentFile[id]).getFailedTests())
        return([],[])
        
    def getPrevSub(self, id):
        if id in self.__studentFile:
            return WeTestObj.WeTestObj.mangoLoad(self.__studentFile[id])._py

# create a test case
class Testcase(WeTestObj.WeTestObj):
    
    def __init__(self,
                 func_name: str, 
                 return_value, 
                 *input_args,
                 dummy=False,):

        super().__init__(dummy)
        
        # implementing the test case
        self.__function_name = func_name
        self.__return_value = return_value
        self.__input_args = input_args

    @classmethod
    def dum(cls):
        return Testcase('', '', dummy=True)

        
    def __repr__(self):
        """ return the test case """
        return f"{self.__function_name}({str(self.__input_args)[1:-1]}) -> {self.__return_value}"
    
    
    def passThisTest(self, func_name: str, Test: 'student module'):
        """ return whether student's py pass the test"""
        # Example: Test.function(a,b)
        test_case_str = lambda x: 'Test.' + func_name + '(' + ','.join([repr(i) for i in x]) + ')'
        try:
            stdAns = eval(test_case_str(self.__input_args))
            if stdAns == self.__return_value:
                return True
            else: return False
        except:
            return False
        
        
    # getter method 
    def getName(self):
        return self.__function_name

    def getReturn(self):
        return self.__return_value
    
    def getInputs(self):
        return self.__input_args





# create a studentFile, including all the info std uploaded
class StudentFile(WeTestObj.WeTestObj):
    
    def __init__(self, id: str, py: str, dummy=False):

        super().__init__(dummy)
        
        self._userid = id
        self._py = py
       
       
        self._passedTest = []
        self._failedTest = []


    @classmethod
    def dum(cls):
        return StudentFile('', '', dummy=True)


    
    def getModule(self):
        # all the students' functions are in the Test module now
        # PAY ATTENTION TO THE DIRECTION
        with open(Global.STUDENT_TEMP_DIR+'StudentFile.py', 'w') as f:
            f.write(self._py.strip())        
        import StudentFile as Test
        return Test
            
    
    @staticmethod
    def checkTest(stdFile, asgmt):
        # run all the testcases for this py
        Test = stdFile.getModule()
        for func_name in asgmt.getFunctions(): # all the func that assigned
            for functions in asgmt.getTestcases().values(): # all the func catagories in the testcase
                for test_func_name, testcaseSerials in functions.items():
                    if test_func_name == func_name:
                        for testcaseSerial in testcaseSerials:
                            testcase = WeTestObj.WeTestObj.mangoLoad(testcaseSerial)
                            if testcase.getName() == func_name:
                                res = testcase.passThisTest(func_name, Test)
                                if res: stdFile._passedTest.append(testcase.serial)
                                else: stdFile._failedTest.append(testcase.serial)
         
    # getter method
    def getPassedTests(self):
        return self._passedTest
    
    
    def getFailedTests(self):
        return self._failedTest
    

    def getId(self):
        return self._userid
        
        
if __name__ == '__main__':
    py = """
            def f():
                return 1

def g(a):
                return a
            """
    x = Assignment('R', 'project1')
    print("Student upload file")

    x.upload('yaoshenx', py)
    x.addSampleTestcase('f', 1)
    x.addSampleTestcase('f', 4, 1, 5)
    x.addSampleTestcase('g', 'a', 1, 6, 'v')
    x.uploadTest('yaoshenx', 'f', 1)
    x.uploadTest('yaoshenx', 'f', 40)
    x.uploadTest('yaoshenx', 'g', 31, 31)
    x.uploadTest('jj', 'g', 2, 6, 7)

    print(x.upload('jj', py))
    print(x.getStdFile())
    print(x.getPrevSub('yaoshenx'))
