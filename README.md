# TestatFs21
###Main class RPNCalculator
####public:
           method:              RPNCalculator()
                                .execute(str, debug = DebugComponents.noDebugging)  executes the string in var str optional param debug

           attribute:          .stack[]                ->  contains allnumbers andvariables <string>for the currentcalculation
                               .variables{}            ->  contains key :variables <string>| value: variablesas value

           static method:      none
           static attribute:   none

 ###private:
           method:             __do_next_calculation() ->  gets the nextstring from thefunctionToExecutelist runs thecorrespondingmethod deletes theuses values fromthe stack andfunctionToExecuteBuild lists. Then appends the result to the stack list.
                               .__get_input_values(str)->  parses the str<string>, returns the next stack values and the next functionToExecute list.

           attribute:          .__function_to_execute[]->  contains all the functions to execute. This list will be empty as the function returns
                               .__function_names{}     ->  maps the function name <string> to the function to be called contains key: type of Operation <string> | value: dictionary with function <dict> -> key: operation <string> | value: corresponding function <?>

           static method:      all calculation methods
           static attribute:   .__const{}              ->  contains all constance the class knows key: constance name <string> | value constance value <float>

###TEST Statistic
    All 87 tests passsed.
    100% lines covered
