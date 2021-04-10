import math
from enum import Enum


# --------------------------
# Enum class for debugging options
# --------------------------
class DebugComponents(Enum):
    noDebugging = 0  # normal operation
    stackBuild = 1  # RPNCalculator.execute() returns the current stack
    variableBuild = 2  # RPNCalculator.execute() returns the current variables
    functionToExecuteBuild = 3  # RPNCalculator.execute() returns the current functionsToExecute
    addVariable = 4  # Adds the variable 'my_var' to .variables{} with the value 9


#                                 (should now always be an empty list)
# --------------------------
# Main class RPNCalculator
#
#
#
# public:
#           method:             RPNCalculator()
#                               .execute(str, debug = DebugComponents.noDebugging)
#                                                       ->  executes the string in var str optional param debug
#
#           attribute:          .stack[]                ->  contains all numbers and variables <string>
#                                                           for the current calculation
#                               .variables{}            ->  contains key :variables <string> | value: variables as value
#
#           static method:      none
#           static attribute:   none
#
# private:
#           method:             __doNextCalculation()   ->  gets the next string from the functionToExecute list
#                                                           runs the corresponding method deletes the uses values
#                                                           from the stack and functionToExecuteBuild lists. Then
#                                                           appends the result to the stack list.
#                               .__getinputvalues(str)  ->  parses the str<string>, returns the next stack values
#                                                           and the next functionToExecute list.
#
#           attribute:          .__functionToExecute[]  ->  contains all the functions to execute. This list will be
#                                                           empty as the function returns
#                               .__functionNames{}      ->  maps the function name <string> to the function to be called
#                                                           contains key: type of Operation
#                                                           <string> | value: dictionary with function <dict> ->
#                                                           key: operation <string> | value: corresponding function <?>
#
#           static method:      all calculation methods
#           static attribute:   .__const{}              ->  contains all constance the class knows
#                                                           key: constance name <string> | value constance value <float>
#
# --------------------------

class RPNCalculator:
    __const = {
        'e': 2.718281828159045,
        'pi': 3.141592653589793,
    }

    def __init__(self):
        self.stack = []
        self.variables = {}
        self.__functionToExecute = []
        self.__functionNames = {
            'dualOperators':
                {
                    '+': RPNCalculator.__add,
                    '-': RPNCalculator.__sub,
                    '*': RPNCalculator.__multiply,
                    '/': RPNCalculator.__divide,
                    '%': RPNCalculator.__modulo,
                    '==': RPNCalculator.__equal,
                    '>=': RPNCalculator.__greaterequalthan,
                    '>': RPNCalculator.__greaterthan,
                    '<=': RPNCalculator.__lessequalthan,
                    '<': RPNCalculator.__lessthan,
                    'pow': math.pow,

                },
            'singleOperators':
                {
                    'abs': RPNCalculator.__abs,
                    'sign': RPNCalculator.__sign,
                    'sin': math.sin,
                    'cos': math.cos,
                    'tan': math.tan,
                    'asin': math.asin,
                    'acos': math.acos,
                    'atan': math.atan,
                    'exp': math.exp,
                    'log': math.log,
                    'log10': math.log10,
                    'sqrt': math.sqrt,
                    'floor': math.floor,
                    'ceil': math.ceil,
                    'round': round,
                    'store': self.__store
                }
        }

    def execute(self, str, debug=DebugComponents.noDebugging):
        if debug == DebugComponents.addVariable:
            self.variables.update({'my_var': 9})
        newValues = self.__getinputvalues(str)
        self.stack.extend(newValues[0])
        self.__functionToExecute.extend(newValues[1])
        if debug == DebugComponents.stackBuild:
            return self.stack

        elif debug == DebugComponents.functionToExecuteBuild:
            return self.__functionToExecute

        while len(self.__functionToExecute) > 0:
            self.stack.append(self.__doNextCalculation())

        return self.stack

    def __doNextCalculation(self):
        if self.__functionToExecute[0] in self.__functionNames['dualOperators'].keys():

            if len(self.stack) < 2:
                print(self.__functionToExecute[0] + " got too few arguments")
                raise TypeError(self.__functionToExecute[0] + " got too few arguments")

            if isinstance(self.stack[-2], str):
                if self.stack[-2] in self.variables.keys():
                    print("loading Variable: " + self.stack[-2] + "-> "  + str(self.variables[self.stack[-2]]))
                    self.stack[-2] = self.variables[self.stack[-2]]
                else:
                    print(
                        self.__functionToExecute[0] + " got invalid arguments " + str(self.stack[-2]) + " " + str(self.stack[-1]))
                    raise TypeError(
                        self.__functionToExecute[0] + " got invalid arguments " + str(self.stack[-2]) + " " + str(self.stack[-1]))

            elif isinstance(self.stack[-1], str):
                if self.stack[-1] in self.variables.keys():
                    print("loading Variable: " + self.stack[-1] + "-> " + str(self.variables[self.stack[-1]]))
                    self.stack[-1] = self.variables[self.stack[-1]]
                else:
                    print(
                        self.__functionToExecute[0] + " got invalid arguments " + str(self.stack[-2]) + " " + str(self.stack[-1]))
                    raise TypeError(
                        self.__functionToExecute[0] + " got invalid arguments " + str(self.stack[-2]) + " " + str(self.stack[-1]))

            result = self.__functionNames['dualOperators'][self.__functionToExecute[0]](self.stack[-2], self.stack[-1])
            self.stack.remove(self.stack[-1])

        elif self.__functionToExecute[0] in self.__functionNames['singleOperators'].keys():
            if len(self.stack) < 1:
                print(self.__functionToExecute[0] + " got too few arguments")
                raise TypeError(self.__functionToExecute[0] + " got too few arguments")

            if isinstance(self.stack[-1], str):
                if self.stack[-1] in self.variables.keys():
                    print("loading Variable: " + self.stack[-1] + "-> " + str(self.variables[self.stack[-1]]))
                    self.stack[-1] = self.variables[self.stack[-1]]
                else:
                    print(self.__functionToExecute[0] + " got invalid arguments " + str(self.stack[-1]))
                    raise TypeError(self.__functionToExecute[0] + " got invalid arguments " + str(self.stack[-1]))

            result = self.__functionNames['singleOperators'][self.__functionToExecute[0]](self.stack[-1])

        else:
            print("Function Not Found!!!!!!")
            raise KeyError("Function not found")

        self.__functionToExecute.remove(self.__functionToExecute[0])
        self.stack.remove(self.stack[-1])
        print("Calculating:")
        print(result)
        return result

    def __getinputvalues(self, str):
        str = str.replace('\n', " ")
        rawinputlist = str.split(" ")
        stacklist = []
        funclist = []

        for element in rawinputlist:
            if len(element) > 0:
                cleanstring = element.lower()
                cleanstring = cleanstring.replace(',', '.')
                if cleanstring.count('.') > 0:
                    stacklist.append(float(cleanstring))
                elif cleanstring.isdigit() or (cleanstring.count('-') > 0 and len(cleanstring) > 1):
                    stacklist.append(int(cleanstring))
                else:
                    if cleanstring[0].isdigit():
                        print('invalid variable name ' + cleanstring)
                        raise SyntaxError('invalid variable name ' + cleanstring)
                    elif cleanstring in self.__functionNames['dualOperators'].keys() or cleanstring in \
                            self.__functionNames['singleOperators'].keys():
                        funclist.append(cleanstring)
                    elif cleanstring in RPNCalculator.__const.keys():
                        stacklist.append(RPNCalculator.__const[cleanstring])
                    else:
                        stacklist.append(cleanstring)
        return [stacklist, funclist]

    # --------------------------
    # Calculation Functions
    # --------------------------

    def __store(self, key):
        indexInStack = len(self.stack)-1
        firstValFound = None
        while firstValFound is not None:
            if not isinstance(self.stack[indexInStack], str):
                firstValFound = self.stack[indexInStack]
            else:
                indexInStack -= 1
        self.variables.update({key : firstValFound})
        return key

    @staticmethod
    def __add(val1, val2):
        return val1 + val2

    @staticmethod
    def __sub(val1, val2):
        return val1 - val2

    @staticmethod
    def __multiply(val1, val2):
        return val1 * val2

    @staticmethod
    def __divide(val1, val2):
        return val1 / val2

    @staticmethod
    def __modulo(val1, val2):
        return val1 % val2

    @staticmethod
    def __equal(val1, val2):
        if val1 == val2:
            return 1
        else:
            return 0

    @staticmethod
    def __greaterequalthan(val1, val2):
        if val1 >= val2:
            return 1
        else:
            return 0

    @staticmethod
    def __greaterthan(val1, val2):
        if val1 > val2:
            return 1
        else:
            return 0

    @staticmethod
    def __lessequalthan(val1, val2):
        if val1 <= val2:
            return 1
        else:
            return 0

    @staticmethod
    def __lessthan(val1, val2):
        if val1 < val2:
            return 1
        else:
            return 0

    @staticmethod
    def __abs(val1):
        if val1 < 0:
            return -1 * val1
        else:
            return val1

    @staticmethod
    def __sign(val1):
        if val1 < 0:
            return -1
        elif val1 > 0:
            return 1
        else:
            return 0
