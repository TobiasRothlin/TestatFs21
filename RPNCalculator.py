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
        text = text.replace('\n', " ")
        rawinputlist = text.split(" ")
        inputlist = []
        for element in rawinputlist:
            if len(element) > 0:
                inputlist.append(RPNCalculator.__classifystirng(element))
        return inputlist

    @staticmethod
    def __classifystirng(text):
        cleanstring = text.lower()
        cleanstring = cleanstring.replace(',', '.')
        if cleanstring.count('.') > 0:
            return float(cleanstring)
        elif cleanstring.isdigit():
            return int(cleanstring)
        else:
            return cleanstring
