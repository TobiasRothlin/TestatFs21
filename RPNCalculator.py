import re


class RPNCalculator:
    def __init__(self):
        self.stack = []
        self.variables = {}

    def execute(self, text):
        self.stack = self.__getinputvalues(text)
        return self.stack

    @staticmethod
    def __getinputvalues(text):
        inputlist = []

        return inputlist


