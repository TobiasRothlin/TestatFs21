import unittest
from RPNCalculator import RPNCalculator
from RPNCalculator import DebugComponents
import io
import sys

class TestCalculator(unittest.TestCase):

    # --------------------------
    # Testing functionality stack
    # --------------------------

    def testStack_IntAndVar(self):
        rpn = RPNCalculator()
        print("Result: ", rpn.execute("1 2 3 my_var", DebugComponents.stackBuild))
        self.assertEqual(rpn.stack, [1, 2, 3, "my_var"])

    def testStack_IntNegNumbers(self):
        rpn = RPNCalculator()
        print("Result: ", rpn.execute("-1 -2 -3 my_var", DebugComponents.stackBuild))
        self.assertEqual(rpn.stack, [-1, -2, -3, "my_var"])

    def testStack_FloatNegNumbers(self):
        rpn = RPNCalculator()
        print("Result: ", rpn.execute("-1.5 -2,1 -3.6 my_var", DebugComponents.stackBuild))
        self.assertEqual(rpn.stack, [-1.5, -2.1, -3.6, "my_var"])

    def testStack_ExcessSpaces(self):
        rpn = RPNCalculator()
        print("Result: ", rpn.execute("1   2   3   my_var", DebugComponents.stackBuild))
        self.assertEqual(rpn.stack, [1, 2, 3, "my_var"])

    def testStack_ExcessSpacesAndNewLines(self):
        rpn = RPNCalculator()
        print("Result: ", rpn.execute("""1   2  \n 3  \nmy_var""", DebugComponents.stackBuild))
        self.assertEqual(rpn.stack, [1, 2, 3, "my_var"])

    def testStack_IntFloatAndVar(self):
        rpn = RPNCalculator()
        print("Result: ", rpn.execute("1 2.0 3 my_var", DebugComponents.stackBuild))
        self.assertEqual(rpn.stack, [1, 2.0, 3, "my_var"])

    def testStack_Int(self):
        rpn = RPNCalculator()
        print("Result: ", rpn.execute("1000 123412 12412311234123 13 14 13", DebugComponents.stackBuild))
        self.assertEqual(rpn.stack, [1000, 123412, 12412311234123, 13, 14, 13])

    def testStack_Var(self):
        rpn = RPNCalculator()
        print("Result: ", rpn.execute("my_var", DebugComponents.stackBuild))
        self.assertEqual(rpn.stack, ["my_var"])

    def testStack_FloatWithCommasAndDecPoint(self):
        rpn = RPNCalculator()
        print("Result: ", rpn.execute("1,2 2.3 3,1 ", DebugComponents.stackBuild))
        self.assertEqual(rpn.stack, [1.2, 2.3, 3.1])

    def testStack_ExcessNewLines(self):
        rpn = RPNCalculator()
        print("Result: ", rpn.execute("1\n2\n\n\n4\n", DebugComponents.stackBuild))
        self.assertEqual(rpn.stack, [1, 2, 4])

    def testStack_InvalidVarName(self):
        rpn = RPNCalculator()
        self.assertRaises(SyntaxError, rpn.execute, *{'1 2 3 5my_var': DebugComponents.stackBuild})

    def testStack_constInput(self):
        rpn = RPNCalculator()
        print("Result: ", rpn.execute("1 2 5 pi e ", DebugComponents.stackBuild))
        self.assertEqual(rpn.stack, [1, 2, 5, 3.141592653589793, 2.718281828159045])

    # End stack test
    # --------------------------
    # Testing functionality single calculations
    # --------------------------

    def testFunction_ToExecute_AddFunction(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 3.0 +", DebugComponents.functionToExecuteBuild)
        print("Result: ", res)
        self.assertEqual(res, ['+'])

    def testFunction_Eval(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 3 4 +")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 7])

    def testFunction_Add(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 3 4 +")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 7])

    def testFunction_Sub(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 3 4 -")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, -1])

    def testFunction_Multiply(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 3 4 *")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 12])

    def testFunction_Divide(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 16 4 /")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 4])

    def testFunction_Modulo(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 15 4 %")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 3])

    def testFunction_Equal(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 15 4 ==")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 0])

    def testFunction_NotEqual(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 4 4 ==")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 1])

    def testFunction_GreaterEqualThan(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 15 4 >=")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 1])

    def testFunction_NotGreaterEqualThan(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 4 14 >=")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 0])

    def testFunction_NotGreaterThan(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 4 14 >")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 0])

    def testFunction_GreaterThan(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 14 4 >")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 1])

    def testFunction_NotGreaterThanWithEqualInput(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 14 14 >")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 0])

    def testFunction_LessEqualThan(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 4 14 <=")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 1])

    def testFunction_NotLessEqualThan(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 14 4 <=")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 0])

    def testFunction_LessThan(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 4 14 <")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 1])

    def testFunction_NotLessThan(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 14 4 <")
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 0])

    def testFunction_AbsNeg(self):
        rpn = RPNCalculator()
        res = rpn.execute("-3 abs")
        print("Result: ", res)
        self.assertEqual(res, [3])

    def testFunction_AbsPos(self):
        rpn = RPNCalculator()
        res = rpn.execute("3 abs")
        print("Result: ", res)
        self.assertEqual(res, [3])

    def testFunction_SignPos(self):
        rpn = RPNCalculator()
        res = rpn.execute("3 sign")
        print("Result: ", res)
        self.assertEqual(res, [1])

    def testFunction_SignZero(self):
        rpn = RPNCalculator()
        res = rpn.execute("0 sign")
        print("Result: ", res)
        self.assertEqual(res, [0])

    def testFunction_SignNeg(self):
        rpn = RPNCalculator()
        res = rpn.execute("-3 sign")
        print("Result: ", res)
        self.assertEqual(res, [-1])

    def testFunction_Sin(self):
        rpn = RPNCalculator()
        res = rpn.execute("90 sin")
        print("Result: ", res)
        self.assertEqual(res, [0.8939966636005579])

    def testFunction_Cos(self):
        rpn = RPNCalculator()
        res = rpn.execute("0 cos")
        print("Result: ", res)
        self.assertEqual(res, [1])

    def testFunction_Tan(self):
        rpn = RPNCalculator()
        res = rpn.execute("0 tan")
        print("Result: ", res)
        self.assertEqual(res, [0])

    def testFunction_Asin(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 asin")
        print("Result: ", res)
        self.assertEqual(res, [1.5707963267948966])

    def testFunction_Acos(self):
        rpn = RPNCalculator()
        res = rpn.execute("0 acos")
        print("Result: ", res)
        self.assertEqual(res, [1.5707963267948966])

    def testFunction_Atan(self):
        rpn = RPNCalculator()
        res = rpn.execute("0 atan")
        print("Result: ", res)
        self.assertEqual(res, [0])

    def testFunction_Exp(self):
        rpn = RPNCalculator()
        res = rpn.execute("2 exp")
        print("Result: ", res)
        self.assertEqual(res, [7.38905609893065])

    def testFunction_Log(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 log")
        print("Result: ", res)
        self.assertEqual(res, [0])

    def testFunction_Log10(self):
        rpn = RPNCalculator()
        res = rpn.execute("10000 log10")
        print("Result: ", res)
        self.assertEqual(res, [4])

    def testFunction_pow(self):
        rpn = RPNCalculator()
        res = rpn.execute("5 7 pow")
        print("Result: ", res)
        self.assertEqual(res, [78125])

    def testFunction_Sqrt(self):
        rpn = RPNCalculator()
        res = rpn.execute("25 sqrt")
        print("Result: ", res)
        self.assertEqual(res, [5])

    def testFunction_Floor(self):
        rpn = RPNCalculator()
        res = rpn.execute("5.999 floor")
        print("Result: ", res)
        self.assertEqual(res, [5])

    def testFunction_Ceil(self):
        rpn = RPNCalculator()
        res = rpn.execute("4.005 ceil")
        print("Result: ", res)
        self.assertEqual(res, [5])

    def testFunction_Round(self):
        rpn = RPNCalculator()
        res = rpn.execute("5.3 round")
        print("Result: ", res)
        self.assertEqual(res, [5])

    # End single calculations test
    # --------------------------
    # Testing functionality multiple calculations
    # --------------------------

    def testMultipleCalculations_1(self):
        rpn = RPNCalculator()
        res = rpn.execute("3 4 5 + +")
        print("Result: ", res)
        self.assertEqual(res, [12])

    def testMultipleCalculations_2(self):
        rpn = RPNCalculator()
        res = rpn.execute("5 3 4 + *")
        print("Result: ", res)
        self.assertEqual(res, [35])

    def testMultipleCalculations_3(self):
        rpn = RPNCalculator()
        res = rpn.execute("5 4 3 - *")
        print("Result: ", res)
        self.assertEqual(res, [5])

    def testMultipleCalculations_4(self):
        rpn = RPNCalculator()
        res = rpn.execute("5 6 14 + /")
        print("Result: ", res)
        self.assertEqual(res, [0.25])

    def testMultipleCalculations_5(self):
        rpn = RPNCalculator()
        rpn.execute("6 14 +")
        res = rpn.execute("5 /")
        print("Result: ", res)
        self.assertEqual(res, [4])

    def testMultipleCalculations_6(self):
        rpn = RPNCalculator()
        rpn.execute("6 14 +")
        res = rpn.execute("13 / round")
        print("Result: ", res)
        self.assertEqual(res, [2])

    def testMultipleCalculations_7(self):
        rpn = RPNCalculator()
        rpn.execute("6")
        rpn.execute("14")
        rpn.execute("+")
        rpn.execute("13")
        rpn.execute("/")
        res = rpn.execute("round")
        print("Result: ", res)
        self.assertEqual(res, [2])

    # End multiple calculations test
    # --------------------------
    # Testing functionality exception handling
    # --------------------------

    def testException_InvalidVarName(self):
        rpn = RPNCalculator()
        self.assertRaises(SyntaxError, rpn.execute, *{'1 2 3 5my_var': DebugComponents.stackBuild})

    def testException_TooFewArgumentsDualOperations(self):
        rpn = RPNCalculator()
        self.assertRaises(TypeError, rpn.execute, *{'2 pow'})

    def testException_TooFewArgumentsSingleOperations(self):
        rpn = RPNCalculator()
        self.assertRaises(TypeError, rpn.execute, *{'abs'})

    def testException_WrongArgumentsSingleOperations(self):
        rpn = RPNCalculator()
        self.assertRaises(TypeError, rpn.execute, *{'hallo abs'})

    def testException_SingleWrongArgumentsDualOperations(self):
        rpn = RPNCalculator()
        self.assertRaises(TypeError, rpn.execute, *{'2 hello pow'})

    def testException_WrongArgumentsDualOperations(self):
        rpn = RPNCalculator()
        self.assertRaises(TypeError, rpn.execute, *{'hello1 hello2 pow'})

    # End exception handling test
    # --------------------------
    # Testing functionality accessing variables
    # --------------------------

    def testVarOps_AccessingVarDualOperation1(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 3 my_var +", DebugComponents.addVariable)
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 12])

    def testVarOps_AccessingVarDualOperation(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 my_var 3 +", DebugComponents.addVariable)
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 12])

    def testVarOps_AccessingVarSingleOperation(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 my_var sqrt", DebugComponents.addVariable)
        print("Result: ", res)
        self.assertEqual(res, [1, 2, 3])

    # End accessing variables test
    # --------------------------
    # Testing functionality stack manipulations
    # --------------------------

    def testVarOps_StoringVar(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 10 20 y store x store")
        print("Result: ", rpn.variables)
        self.assertEqual(rpn.variables, {"y": 20, "x": 10})

    def testVarOps_LoadingVar(self):
        rpn = RPNCalculator()
        res = rpn.execute("my_var load", DebugComponents.addVariable)
        print("Result: ", res)
        self.assertEqual(res, [9])

    def testVarOps_LoadingNotDefinedVar(self):
        rpn = RPNCalculator()
        rpn.execute("",DebugComponents.addVariable)
        self.assertRaises(NameError, rpn.execute, *{"speed load"})

    def testStackOps_ClearStack(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 3 4 5")
        self.assertEqual(rpn.stack, [1, 2, 3, 4, 5])
        rpn.execute("clear")
        print("Result: ", rpn.stack)
        self.assertEqual(rpn.stack, [])

    def testStackOps_SwapStack(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 3 4 5")
        self.assertEqual(rpn.stack, [1, 2, 3, 4, 5])
        rpn.execute("swap")
        print("Result: ", rpn.stack)
        self.assertEqual(rpn.stack, [1, 2, 3, 5, 4])

    def testStackOps_DropStack(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 3 4 5")
        self.assertEqual(rpn.stack, [1, 2, 3, 4, 5])
        rpn.execute("drop")
        print("Result: ", rpn.stack)
        self.assertEqual(rpn.stack, [1, 2, 3, 4])

    def testStackOps_DupStack(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 3 4 5")
        self.assertEqual(rpn.stack, [1, 2, 3, 4, 5])
        rpn.execute("dup")
        print("Result: ", rpn.stack)
        self.assertEqual(rpn.stack, [1, 2, 3, 4, 5, 5])

    def testStackOps_OverStack(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 3 4 5")
        self.assertEqual(rpn.stack, [1, 2, 3, 4, 5])
        rpn.execute("over")
        print("Result: ", rpn.stack)
        self.assertEqual(rpn.stack, [1, 2, 3, 4, 5, 4])

    def testStackOps_RotStack(self):
        rpn = RPNCalculator()
        res = rpn.execute("1 2 3 4 5")
        self.assertEqual(rpn.stack, [1, 2, 3, 4, 5])
        rpn.execute("rot")
        print("Result: ", rpn.stack)
        self.assertEqual(rpn.stack, [1, 2, 4, 5, 3])

    # End stack manipulations test
    # --------------------------
    # Testing functionality runfile
    # --------------------------

    def testRunfile_testHypoFile(self):
        rpn = RPNCalculator()
        res = rpn.execute("3 4")
        rpn.run_file("hypotenuse.rpn")
        print("Result: ", rpn.stack)
        self.assertEqual(rpn.stack, [5.0])

    # End runfile test
    # --------------------------
    # Testing functionality print Stack
    # --------------------------

    def testPrintStack_testOutput(self):
        rpn = RPNCalculator()
        rpn.execute("10 20 30.0")
        print("Result: ", str(rpn))
        self.assertEqual(str(rpn), "3: 10\n2: 20\n1: 30.0")

if __name__ == '__main__':
    unittest.main()
