from enum import Enum
import re

# Enums for Keyword and Token Types
class KeywordType(Enum):
    CLASS = "class"
    METHOD = "method"
    FUNCTION = "function"
    CONSTRUCTOR = "constructor"
    INT = "int"
    BOOLEAN = "boolean"
    CHAR = "char"
    VOID = "void"
    VAR = "var"
    STATIC = "static"
    FIELD = "field"
    LET = "let"
    DO = "do"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    RETURN = "return"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    THIS = "this"


class TokenType(Enum):
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    IDENTIFIER = "IDENTIFIER"
    INT_CONST = "INT_CONST"
    STRING_CONST = "STRING_CONST"


class JackTokenizer:
    KEYWORDS = {
        "class", "constructor", "function", "method", "field", "static",
        "var", "int", "char", "boolean", "void", "true", "false", "null",
        "this", "let", "do", "if", "else", "while", "return"
    }
    SYMBOLS = "{}()[].,;+-*/&|<>=~"
    OPERATIONS = "+-*/&|<>=~"

    def __init__(self, filename: str):
        """Initializes the tokenizer with a file."""
        with open(filename, 'r') as file:
            self.lines = file.readlines()

        self.tokens = []
        self.current_token = None
        self.pointer = 0
        self._tokenize()

    def _tokenize(self):
        """Tokenizes the entire file content."""
        code = ''.join(self.lines)
        # Remove comments
        code = re.sub(r'//.*|/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'\n', ' ', code)

        # Tokenize using regex
        token_pattern = r'("[^"\n]*")|([{}()[\].,;+\-*/&|<>=~])|(\d+)|([a-zA-Z_]\w*)'
        matches = re.findall(token_pattern, code)

        for match in matches:
            string, symbol, integer, identifier = match
            if string:
                self.tokens.append(string)
            elif symbol:
                self.tokens.append(symbol)
            elif integer:
                self.tokens.append(integer)
            elif identifier:
                self.tokens.append(identifier)

    def hasMoreTokens(self) -> bool:
        """Checks if there are more tokens to process."""
        return self.pointer < len(self.tokens)

    def advance(self):
        """Moves to the next token."""
        if self.hasMoreTokens():
            self.current_token = self.tokens[self.pointer]
            self.pointer += 1

    def tokenType(self) -> TokenType:
        """Returns the type of the current token."""
        if self.current_token in self.KEYWORDS:
            return TokenType.KEYWORD
        elif self.current_token in self.SYMBOLS:
            return TokenType.SYMBOL
        elif self.current_token.isdigit():
            return TokenType.INT_CONST
        elif self.current_token.startswith('"') and self.current_token.endswith('"'):
            return TokenType.STRING_CONST
        else:
            return TokenType.IDENTIFIER

    def keyWord(self) -> KeywordType:
        """Returns the current token if it is a keyword."""
        if self.tokenType() == TokenType.KEYWORD:
            return KeywordType(self.current_token)

    def symbol(self) -> str:
        """Returns the current token if it is a symbol."""
        if self.tokenType() == TokenType.SYMBOL:
            return self.current_token

    def identifier(self) -> str:
        """Returns the current token if it is an identifier."""
        if self.tokenType() == TokenType.IDENTIFIER:
            return self.current_token

    def intVal(self) -> int:
        """Returns the integer value of the current token."""
        if self.tokenType() == TokenType.INT_CONST:
            return int(self.current_token)

    def stringVal(self) -> str:
        """Returns the string value of the current token."""
        if self.tokenType() == TokenType.STRING_CONST:
            return self.current_token.strip('"')

    def decrementPointer(self):
        """Moves the token pointer back by one."""
        if self.pointer > 0:
            self.pointer -= 1
            self.current_token = self.tokens[self.pointer]

    def isOperation(self) -> bool:
        """Checks if the current symbol is an operation."""
        if self.tokenType() == TokenType.SYMBOL and self.current_token in self.OPERATIONS:
            return True
        return False
