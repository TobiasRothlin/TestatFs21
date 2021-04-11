import math
from enum import Enum


# --------------------------
# Enum class for debugging options
# --------------------------
class DebugComponents(Enum):
    noDebugging = 0  # normal operation
    stackBuild = 1  # RPNCalculator.execute() returns the current stack
    variableBuild = 2  # RPNCalculator.execute() returns the current variables
    functionToExecuteBuild = 3  # RPNCalculator.execute() returns the current
    #                                 functionsToExecute
    addVariable = 4  # Adds the variable 'my_var' to .variables{}


#                      with the value 9
#                                 (should now always be an empty list)
# --------------------------
# Main class RPNCalculator
#
#
#
# public:
#           method:             RPNCalculator()
#                               .execute(str, debug =
#                               DebugComponents.noDebugging)
#                                                       ->  executes the string
#                                                       in var str optional
#                                                       param debug
#
#           attribute:          .stack[]                ->  contains all
#                                                           numbers and
#                                                           variables <string>
#                                                           for the current
#                                                           calculation
#                               .variables{}            ->  contains key :
#                                                           variables <string>
#                                                           | value: variables
#                                                           as value
#
#           static method:      none
#           static attribute:   none
#
# private:
#           method:             __do_next_calculation() ->  gets the next
#                                                           string from the
#                                                           functionToExecute
#                                                           list runs the
#                                                           corresponding
#                                                           method deletes the
#                                                           uses values from
#                                                           the stack and
#                                                        functionToExecuteBuild
#                                                           lists. Then
#                                                           appends the result
#                                                           to the stack list.
#                               .__get_input_values(str)->  parses the
#                                                           str<string>,
#                                                           returns the next
#                                                           stack values
#                                                           and the next
#                                                           functionToExecute
#                                                           list.
#
#           attribute:          .__function_to_execute[]->  contains all the
#                                                           functions to
#                                                           execute. This list
#                                                           will be empty as
#                                                           the function
#                                                           returns
#                               .__function_names{}     ->  maps the function
#                                                           name <string> to
#                                                           the function to be
#                                                           called contains
#                                                           key: type of
#                                                           Operation
#                                                           <string> | value:
#                                                           dictionary with
#                                                           function <dict> ->
#                                                           key: operation
#                                                           <string> | value:
#                                                           corresponding
#                                                           function <?>
#
#           static method:      all calculation methods
#           static attribute:   .__const{}              ->  contains all
#                                                           constance the
#                                                           class knows
#                                                           key: constance
#                                                           name <string> |
#                                                           value constance
#                                                           value <float>
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
        self.__function_to_execute = []
        self.__function_names = {
            'dualOperators':
                {
                    '+': RPNCalculator.__add,
                    '-': RPNCalculator.__sub,
                    '*': RPNCalculator.__multiply,
                    '/': RPNCalculator.__divide,
                    '%': RPNCalculator.__modulo,
                    '==': RPNCalculator.__equal,
                    '>=': RPNCalculator.__greater_equal_than,
                    '>': RPNCalculator.__greater_than,
                    '<=': RPNCalculator.__less_equal_than,
                    '<': RPNCalculator.__less_than,
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

                },
            'stackOperations':
                {
                    'store': self.__store,
                    'load': self.__load,
                    'clear': self.__clear,
                    'drop': self.__drop,
                    'dup': self.__dup,
                    'swap': self.__swap,
                    'over': self.__over,
                    'rot': self.__rot
                }
        }

    def execute(self, string, debug=DebugComponents.noDebugging):
        if debug == DebugComponents.addVariable:
            self.variables.update({'my_var': 9})
        new_values = self.__get_input_values(string)
        self.stack.extend(new_values[0])
        self.__function_to_execute.extend(new_values[1])
        if debug == DebugComponents.stackBuild:
            return self.stack

        elif debug == DebugComponents.functionToExecuteBuild:
            return self.__function_to_execute

        while len(self.__function_to_execute) > 0:
            res = self.__do_next_calculation
            if res is not None:
                self.stack.append(res)

        return self.stack

    def run_file(self, fname):
        file = open(fname, "r")
        for line in file:
            if not line[0] == '#':
                print("Executing next line file: ", line)
                self.execute(line)
        file.close()
        return self.stack

    @property
    def __do_next_calculation(self):
        result = None
        if self.__function_to_execute[0] in \
                self.__function_names['dualOperators'].keys():

            if len(self.stack) < 2:
                print(self.__function_to_execute[0] + " got too few arguments")
                raise TypeError(
                    self.__function_to_execute[0] + " got too few arguments")

            if isinstance(self.stack[-2], str):
                if self.stack[-2] in self.variables.keys():
                    print("loading Variable: " + self.stack[-2] + "-> " + str(
                        self.variables[self.stack[-2]]))
                    self.stack[-2] = self.variables[self.stack[-2]]
                else:
                    print(
                        self.__function_to_execute[
                            0] + " got invalid arguments " + str(
                            self.stack[-2]) + " " + str(
                            self.stack[-1]))

                    raise TypeError(
                        self.__function_to_execute[
                            0] + " got invalid arguments " + str(
                            self.stack[-2]) + " " + str(
                            self.stack[-1]))

            elif isinstance(self.stack[-1], str):
                if self.stack[-1] in self.variables.keys():
                    print("loading Variable: " + self.stack[-1] + "-> " + str(
                        self.variables[self.stack[-1]]))
                    self.stack[-1] = self.variables[self.stack[-1]]
                else:
                    print(
                        self.__function_to_execute[
                            0] + " got invalid arguments " + str(
                            self.stack[-2]) + " " + str(
                            self.stack[-1]))
                    raise TypeError(
                        self.__function_to_execute[
                            0] + " got invalid arguments " + str(
                            self.stack[-2]) + " " + str(
                            self.stack[-1]))

            result = self.__function_names['dualOperators'][
                self.__function_to_execute[0]](self.stack[-2],
                                               self.stack[-1])
            self.stack.remove(self.stack[-1])

        elif self.__function_to_execute[0] in \
                self.__function_names['singleOperators'].keys():
            if len(self.stack) < 1:
                print(self.__function_to_execute[0] + " got too few arguments")
                raise TypeError(
                    self.__function_to_execute[0] + " got too few arguments")

            if isinstance(self.stack[-1], str):
                if self.stack[-1] in self.variables.keys():
                    print("loading Variable: " + self.stack[-1] + "-> " + str(
                        self.variables[self.stack[-1]]))
                    self.stack[-1] = self.variables[self.stack[-1]]
                else:
                    print(self.__function_to_execute[
                              0] + " got invalid arguments " + str(
                        self.stack[-1]))
                    raise TypeError(self.__function_to_execute[
                                        0] + " got invalid arguments " + str(
                        self.stack[-1]))

            result = self.__function_names['singleOperators'][
                self.__function_to_execute[0]](self.stack[-1])

        elif self.__function_to_execute[0] in \
                self.__function_names['stackOperations'].keys():
            res = self.__function_names['stackOperations'][
                self.__function_to_execute[0]]()
            self.__function_to_execute.remove(self.__function_to_execute[0])
            return res

        self.__function_to_execute.remove(self.__function_to_execute[0])
        self.stack.remove(self.stack[-1])
        print("Calculating:")
        print(result)
        return result

    def __get_input_values(self, string):
        string = string.replace('\n', " ")
        raw_input_list = string.split(" ")
        stack_list = []
        func_list = []

        for element in raw_input_list:
            if len(element) > 0:
                clean_string = element.lower()
                clean_string = clean_string.replace(',', '.')
                if clean_string.count('.') > 0:
                    stack_list.append(float(clean_string))
                elif clean_string.isdigit() or (
                        clean_string.count('-') > 0 and len(clean_string) > 1):
                    stack_list.append(int(clean_string))
                else:
                    if clean_string[0].isdigit():
                        print('invalid variable name ' + clean_string)
                        raise SyntaxError(
                            'invalid variable name ' + clean_string)
                    elif clean_string in self.__function_names[
                        'dualOperators'].keys() or clean_string in \
                            self.__function_names[
                                'singleOperators'].keys() or clean_string in \
                            self.__function_names['stackOperations'].keys():
                        func_list.append(clean_string)
                    elif clean_string in RPNCalculator.__const.keys():
                        stack_list.append(RPNCalculator.__const[clean_string])
                    else:
                        stack_list.append(clean_string)
        return [stack_list, func_list]

    def __str__(self):
        current_index = len(self.stack)
        print_string = ""
        for element in self.stack[:-1]:
            print_string += str(current_index) + ": " + str(element) + "\n"
            current_index -= 1
        print_string += str(current_index) + ": " + str(self.stack[-1])
        return print_string

    # --------------------------
    # Stack Operations
    # --------------------------

    def __store(self):
        first_number_in_stack = None
        current_index_in_stack = -1
        while first_number_in_stack is None:
            if not isinstance(self.stack[current_index_in_stack], str):
                first_number_in_stack = self.stack[current_index_in_stack]
            else:
                current_index_in_stack -= 1
                if len(self.stack)+current_index_in_stack < 0:
                    raise TypeError("No number in stack to store")
        self.variables.update(
            {self.stack[current_index_in_stack + 1]: first_number_in_stack})
        self.stack.remove(self.stack[current_index_in_stack])
        self.stack.remove(self.stack[current_index_in_stack + 1])
        return

    def __load(self):
        if self.stack[-1] in self.variables.keys():
            load_number = self.variables[self.stack[-1]]
            self.stack.remove(self.stack[-1])
            return load_number
        else:
            raise NameError(
                "variable '" + str(self.stack[-1]) + "' is not defined")

    def __clear(self):
        self.stack.clear()
        return

    def __drop(self):
        if len(self.stack) > 0:
            self.stack.remove(self.stack[-1])
        return

    def __dup(self):
        if len(self.stack) > 0:
            self.stack.append(self.stack[-1])
        return

    def __swap(self):
        if len(self.stack) > 0:
            if len(self.stack) > 1:
                temp = self.stack[-1]
                self.stack[-1] = self.stack[-2]
                self.stack[-2] = temp
            else:
                return
        else:
            print(
                "the swap command needs 2 or more elements on the stack "
                "currently only " + str(
                    len(self.stack)) + " elements on the stack")
            raise TypeError(
                "the swap command needs 2 or more elements on the stack "
                "currently only " + str(
                    len(self.stack)) + " elements on the stack")
        return

    def __over(self):
        if len(self.stack) > 1:
            self.stack.append(self.stack[-2])
        else:
            print(
                "the over command needs 2 or more elements on the stack "
                "currently only " + str(
                    len(self.stack)) + " elements on the stack")
            raise TypeError(
                "the over command needs 2 or more elements on the stack "
                "currently only " + str(
                    len(self.stack)) + " elements on the stack")
        return

    def __rot(self):
        if len(self.stack) > 2:
            temp = self.stack[-3]
            self.stack[-3] = self.stack[-2]
            self.stack[-2] = self.stack[-1]
            self.stack[-1] = temp
        else:
            print(
                "the rot command needs 3 or more elements on the stack "
                "currently only " + str(
                    len(self.stack)) + " elements on the stack")
            raise TypeError(
                "the rot command needs 3 or more elements on the stack "
                "currently only " + str(
                    len(self.stack)) + " elements on the stack")
        return

    # --------------------------
    # Calculation Functions
    # --------------------------

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
    def __greater_equal_than(val1, val2):
        if val1 >= val2:
            return 1
        else:
            return 0

    @staticmethod
    def __greater_than(val1, val2):
        if val1 > val2:
            return 1
        else:
            return 0

    @staticmethod
    def __less_equal_than(val1, val2):
        if val1 <= val2:
            return 1
        else:
            return 0

    @staticmethod
    def __less_than(val1, val2):
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
