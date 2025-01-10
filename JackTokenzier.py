import re

COMMENT_REGEX = r"(//.*)|(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)"
EMPTY_PATTERN = re.compile(r"\s*")
KEYWORD_MATCH = re.compile(r"^\s*("
                            r"class|constructor|function|method|static|field"
                            r"|var|int|char|boolean|void|true|false|null|this|"
                            r"let|do|if|else|while|return)\s*")
SYMBOL_MATCH = re.compile(r"^\s*([{}()\[\].,;+\-*/&|<>=~])\s*")
NUMBER_MATCH = re.compile(r"^\s*(\d+)\s*")
STRING_MATCH = re.compile(r"^\s*\"(.*)\"\s*")
IDENTIFIER_MATCH = re.compile(r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*")

DEBUG_MODE = False

class JackTokenizer:
    """
    JackTokenizer module as described in NAND2Tetris chapter 10
    """

    keyword = ["CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT",
                "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET",
                "DO", "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE",
                "NULL", "THIS"]

    KEYWORD = 0
    SYMBOL = 1
    INT_CONST = 2
    STRING_CONST = 3
    IDENTIFIER = 4

    def __init__(self, input_file_path):
        """
        :param input_file: the current file
        """
        with open(input_file_path, "r") as file:
            self.text = file.read()
        self._clear_all_comments()
        self._tokenType = None
        self._currentToken = None

    def _clear_all_comments(self):
        """
        Clear all comments from self.text .
        """
        self.text = re.sub(COMMENT_REGEX, "", self.text)

    def hasMoreTokens(self):
        if re.fullmatch(EMPTY_PATTERN, self.text):
            return False
        else:
            return True

    def advance(self):
        if self.hasMoreTokens():
            current_match = re.match(KEYWORD_MATCH, self.text)
            if current_match is not None:
                self.text = re.sub(KEYWORD_MATCH, "", self.text)
                self._tokenType = JackTokenizer.KEYWORD
                self._currentToken = current_match.group(1)
            else:
                current_match = re.match(SYMBOL_MATCH, self.text)
                if current_match is not None:
                    self.text = re.sub(SYMBOL_MATCH, "", self.text)
                    self._tokenType = JackTokenizer.SYMBOL
                    self._currentToken = current_match.group(1)
                else:
                    current_match = re.match(NUMBER_MATCH, self.text)
                    if current_match is not None:
                        self.text = re.sub(NUMBER_MATCH, "", self.text)
                        self._tokenType = JackTokenizer.INT_CONST
                        self._currentToken = current_match.group(1)
                    else:
                        current_match = re.match(STRING_MATCH, self.text)
                        if current_match is not None:
                            self.text = re.sub(STRING_MATCH, "", self.text)
                            self._tokenType = JackTokenizer.STRING_CONST
                            self._currentToken = current_match.group(1)
                        else:
                            current_match = re.match(IDENTIFIER_MATCH, self.text)
                            if current_match is not None:
                                self.text = re.sub(IDENTIFIER_MATCH, "", self.text)
                                self._tokenType = JackTokenizer.IDENTIFIER
                                self._currentToken = current_match.group(1)

    def tokenType(self):
        return self._tokenType

    def keyWord(self):
        return self._currentToken

    def symbol(self):
        return self._currentToken

    def identifier(self):
        return self._currentToken

    def intVal(self):
        return int(self._currentToken)

    def stringVal(self):
        return self._currentToken


