import unittest
from RPNCalculator import RPNCalculator


class TestCalculator(unittest.TestCase):
    def testStack_IntAndVar(self):
        rpn = RPNCalculator()
        self.assertEqual(rpn.execute("1 2 3 my_var"), [1, 2, 3, "my_var"])

    def testStack_ExcessSpaces(self):
        rpn = RPNCalculator()
        self.assertEqual(rpn.execute("1   2   3   my_var"), [1, 2, 3, "my_var"])

    def testStack_IntFloatAndVar(self):
        rpn = RPNCalculator()
        self.assertEqual(rpn.execute("1 2.0 3 my_var"), [1, 2.0, 3, "my_var"])

    def testStack_Int(self):
        rpn = RPNCalculator()
        self.assertEqual(rpn.execute("1000 123412 12412311234123 13 14 13"), [1000, 123412, 12412311234123, 13, 14, 13])

    def testStack_Var(self):
        rpn = RPNCalculator()
        self.assertEqual(rpn.execute("my_var"), ["my_var"])

    def testStack_IntAndVar(self):
        rpn = RPNCalculator()
        self.assertEqual(rpn.execute("1 2 3 my_var"), [1, 2, 3, "my_var"])

    def testStack_IntAndVar(self):
        rpn = RPNCalculator()
        self.assertEqual(rpn.execute("1 2 3 my_var"), [1, 2, 3, "my_var"])




if __name__ == '__main__':
    unittest.main()
