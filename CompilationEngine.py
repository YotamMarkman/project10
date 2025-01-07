


from JackTokenzier import *

class CompilationEngine:
    def __init__(self, input_file: str, output_file: str):
        """Initializes with a tokenizer and an output file."""
        self.tokenizer = JackTokenizer(input_file)
        self.output_file = open(output_file, 'w')
        self.first_routine = True

    def compileClass(self):
        """Parses a complete class."""
        self.tokenizer.advance()
        self.output_file.write("<class>\n")
        self.tokenizer.advance()
        self.output_file.write("<keyword> class </keyword>\n")
        self.tokenizer.advance()
        self.output_file.write("<identifier> " + self.tokenizer.current_token.value + " </identifier>\n")
        self.tokenizer.advance()
        self.output_file.write("<symbol> { </symbol>\n")
        self.compileClassVarDec()
        self.output_file.write("<symbol } </symbol>\n")
        self.tokenizer.advance()
        self.output_file.write("<class>\n")
        self.output_file.close()

    def compileClassVarDec(self):
        """Parses a static variable or field declaration."""
        self.tokenizer.advance()
        self.output_file.write("<classVarDec>\n")
        match = ["static", "field",]
        if self.tokenizer.current_token.value == match:
            self.output_file.write("<keyword> " + self.tokenizer.current_token.value + " </keyword>\n")
            self.tokenizer.advance()
            self.output_file.write("<identifier> " + self.tokenizer.current_token.value + " </identifier>\n")
            self.tokenizer.advance()
            if self.tokenizer.current_token.value == ",":
                self.output_file.write("<symbol> , </symbol>\n")
                self.tokenizer.advance()
                self.output_file.write("<identifier> " + self.tokenizer.current_token.value + " </identifier>\n")
                self.tokenizer.advance()
            self.output_file.write("<symbol> ; </symbol>\n")
            self.tokenizer.advance()
            self.output_file.write("</classVarDec>\n")

    def compileSubroutine(self):
        """Parses a complete method, function, or constructor."""
        match = ["constructor", "function", "method",]
        self.tokenizer.advance()
        self.output_file.write("<subroutineDec>\n")
        if self.tokenizer.current_token.value == match:
            self.output_file.write("<keyword> " + match + " </keyword>\n")
            self.tokenizer.advance()
            self.output_file.write("<keyword> " + self.tokenizer.current_token.value + " </keyword>\n")
            self.tokenizer.advance()
            self.output_file.write("<identifier> " + self.tokenizer.current_token.value + " </identifier>\n")
            self.tokenizer.advance()
            self.output_file.write("<symbol> ( </symbol>\n")
            self.compileParameterList()
            self.output_file.write("<symbol> ) </symbol>\n")
            self.compileSubroutineBody()
            self.output_file.write("</subroutineDec>\n")

    def compileParameterList(self):
        """Parses a parameter list."""
        self.tokenizer.advance()
        self.output_file.write("<parameterList>\n")
        while self.tokenizer.current_token.value != ")":
            self.output_file.write("<keyword> " + self.tokenizer.current_token.value + " </keyword>\n")
            self.tokenizer.advance()
            self.output_file.write("<identifier> " + self.tokenizer.current_token.value + " </identifier>\n")
            self.tokenizer.advance()
            if self.tokenizer.current_token.value == ",":
                self.output_file.write("<symbol> , </symbol>\n")
                self.tokenizer.advance()

    def compileSubroutineBody(self):
        """Parses a complete subroutine body."""
        self.tokenizer.advance()
        self.output_file.write("<subroutineBody>\n")
        self.output_file.write("<symbol> { </symbol>\n")
        self.output_file.write("<statements>\n")
        self.compileStatements()
        self.compileReturn()
        self.output_file.write("</statements>\n")
        self.output_file.write("<symbol> } </symbol>\n")
        self.tokenizer.advance()
        self.output_file.write("</subroutineBody>\n")

    def compileVarDec(self):
        """Parses a variable declaration."""
        pass

    def compileStatements(self):
        """Parses a sequence of statements."""
        self.output_file.write("<returnStatements>\n")
        self.tokenizer.advance()
        self.output_file.write("<keyword> " + self.tokenizer.current_token.value + " </keyword>\n")
        self.tokenizer.advance()
        self.output_file.write("<expression>\n")
        self.compileExpression()
        self.output_file.write("</expression>\n")
        self.output_file.write("<symbol> ; </symbol>\n")
        self.tokenizer.advance()
        self.output_file.write("</returnStatements>\n")

    def compileLet(self):
        """Parses a 'let' statement."""
        self.output_file.write("<keyword>" + self.tokenizer.current_token.value + "</keyword>\n")
        self.tokenizer.advance()
        self.output_file.write("<identifier>" + self.tokenizer.current_token.value + "</identifier>\n")
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == "symbol" and self.tokenizer.current_token.value == "[":
            self.output_file.write("<symbol>" + self.tokenizer.current_token.value + "</symbol>\n")
            self.compileExpression()
            if self.tokenizer.tokenType() == "symbol" and self.tokenizer.current_token.value == "]":
                self.output_file.write("<symbol>" + self.tokenizer.current_token.value + "</symbol>\n")
            self.tokenizer.advance()
        self.output_file.write("<symbol>" + self.tokenizer.current_token.value + "</symbol>\n")
        self.compileExpression()
        self.output_file.write("<symbol>" + self.tokenizer.current_token.value + "</symbol>\n")
        self.tokenizer.advance()

    def compileWhile(self):
        """Parses a 'while' statement."""


    def compileDo(self):
        """Parses a 'do' statement."""
        pass

    def compileReturn(self):
        """Parses a 'return' statement."""
        pass

    def compileIf(self):
        """Parses an 'if' statement."""
        pass

    def compileExpression(self):
        """Parses an expression."""
        pass

    def compileTerm(self):
        """Parses a term."""
        pass

    def compileExpressionList(self):
        """Parses an expression list."""
        pass
