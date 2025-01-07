


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
        if self.tokenizer.current_token.value in match:
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
        if self.tokenizer.current_token.value in match:
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
        self.output_file.write("<varDec>\n")
        self.tokenizer.advance()
        self.output_file.write("<keyword> var </keyword>\n")
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == "identifier":
            self.output_file.write("<identifier> " + self.tokenizer.current_token.value + " </identifier>\n")
            self.tokenizer.advance()



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
        self.output_file.write("<statement> <letStatement>")
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
        self.output_file.write("</letStatement> </statement>\n")

    def compileWhile(self):
        """Parses a 'while' statement."""
        self.output_file.write("<whileStatement>")
        self.tokenizer.advance()
        self.output_file.write("<keyword>" + self.tokenizer.current_token.value + "</keyword>\n")
        self.tokenizer.advance()
        self.output_file.write("<symbol>" + self.tokenizer.current_token.value + "</symbol>\n")
        self.compileExpression()
        self.output_file.write("<symbol>" + self.tokenizer.current_token.value + "</symbol>\n")
        self.tokenizer.advance()
        self.output_file.write("<symbol> { </symbol>\n")
        self.output_file.write("<statements>\n")
        self.compileStatements()
        self.output_file.write("</statements>\n")
        self.output_file.write("<symbol> } </symbol>\n")
        self.tokenizer.advance()
        self.output_file.write("</whileStatement>\n")

    def compileDo(self):
        """Parses a 'do' statement."""
        self.output_file.write("<doStatement>")
        self.tokenizer.advance()
        self.output_file.write("<keyword>" + self.tokenizer.current_token.value + "</keyword>\n")
        self.tokenizer.advance()
        self.output_file.write("<identifier>" + self.tokenizer.current_token.value + "</identifier>\n")
        self.tokenizer.advance()
        self.output_file.write("<symbol>" + self.tokenizer.current_token.value + "</symbol>\n")
        self.tokenizer.advance()
        self.output_file.write("<identifier>" + self.tokenizer.current_token.value + "</identifier>\n")
        self.tokenizer.advance()
        self.output_file.write("<symbol> ( </symbol>\n")
        for i in range(self.compileExpressionList()):
            self.output_file.write("<expression>\n")
            self.compileExpression()
            self.output_file.write("</expression>\n")
            self.output_file.write("<symbol>" + self.tokenizer.current_token.value + "</symbol>\n")
        self.output_file.write("<symbol> ) </symbol>\n")
        self.tokenizer.advance()
        self.output_file.write("</doStatement>\n")

    def compileReturn(self):
        """Parses a 'return' statement."""
        self.output_file.write("<returnStatement>")
        self.tokenizer.advance()
        self.output_file.write("<keyword>" + "return" + "</keyword>\n")
        self.tokenizer.advance()
        if self.tokenizer.current_token.value != ";":
            self.compileExpression()
        self.output_file.write("<symbol>" + self.tokenizer.current_token.value + "</symbol>\n")
        self.tokenizer.advance()
        self.output_file.write("</returnStatement>\n")


    def compileIf(self):
        """Parses an 'if' statement."""
        self.output_file.write("<ifStatement>")
        self.tokenizer.advance()
        self.output_file.write("<keyword>" + "if" + "</keyword>\n")
        self.tokenizer.advance()
        self.output_file.write("<symbol>" + self.tokenizer.current_token.value + "</symbol>\n")
        self.compileExpression()
        self.output_file.write("<symbol>" + self.tokenizer.current_token.value + "</symbol>\n")
        self.tokenizer.advance()
        self.output_file.write("<symbol> { </symbol>\n")
        self.output_file.write("<statements>\n")
        self.compileStatements()
        self.output_file.write("</statements>\n")
        self.output_file.write("<symbol> } </symbol>\n")
        self.tokenizer.advance()
        if self.tokenizer.current_token.value == "else":
            self.output_file.write("<keyword>" + "else" + "</keyword>\n")
            self.tokenizer.advance()
            self.output_file.write("<symbol>" + self.tokenizer.current_token.value + "</symbol>\n")
            self.tokenizer.advance()
            self.output_file.write("<statements>\n")
            self.compileStatements()
            self.output_file.write("</statements>\n")
            self.output_file.write("<symbol>" + "}" + "</symbol>\n")
            self.tokenizer.advance()
        self.output_file.write("</ifStatement>")

    def compileExpression(self):
        """Parses an expression."""
        self.output_file.write("<expression>\n")
        self.compileTerm()

        while True:
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == "symbol" and self.tokenizer.current_token.value in ['+', '-', '*', '/', '&', '|', '<', '>','=']:
                if self.tokenizer.current_token.value == '<':
                    self.output_file.write("<symbol> &lt; </symbol>\n")
                elif self.tokenizer.current_token.value == '>':
                    self.output_file.write("<symbol> &gt; </symbol>\n")
                elif self.tokenizer.current_token.value == '&':
                    self.output_file.write("<symbol> &amp; </symbol>\n")
                else:
                    self.output_file.write(f"<symbol> {self.tokenizer.current_token.value} </symbol>\n")

                self.compileTerm()
            else:
                self.tokenizer.decrementPointer()
                break

            self.output_file.write("</expression>\n")

    def compileTerm(self):
        """Parses a term."""
        self.output_file.write("<term>\n")
        self.tokenizer.advance()
        if self.tokenizer.tokenType() == "identifier":
            prev_identifier = self.tokenizer.current_token.value
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == "symbol" and self.tokenizer.current_token.value == '[':
                # Array access
                self.output_file.write(f"<identifier> {prev_identifier} </identifier>\n")
                self.output_file.write("<symbol> [ </symbol>\n")
                self.compileExpression()
                self.tokenizer.advance()
                self.output_file.write("<symbol> ] </symbol>\n")
            elif self.tokenizer.tokenType() == "symbol" and self.tokenizer.current_token.value in ['(', '.']:
                # Subroutine call
                self.tokenizer.decrementPointer()
                self.tokenizer.decrementPointer()
                self.compileDo()
            else:
                # Simple identifier
                self.output_file.write(f"<identifier> {prev_identifier} </identifier>\n")
                self.tokenizer.decrementPointer()
        elif self.tokenizer.tokenType() == "integerConstant":
            self.output_file.write(f"<integerConstant> {self.tokenizer.current_token.value} </integerConstant>\n")
        elif self.tokenizer.tokenType() == "stringConstant":
            self.output_file.write(f"<stringConstant> {self.tokenizer.current_token.value} </stringConstant>\n")
        elif self.tokenizer.tokenType() == "keyword" and self.tokenizer.current_token.value in ["true", "false", "null",                                                                                 "this"]:
            self.output_file.write(f"<keyword> {self.tokenizer.current_token.value} </keyword>\n")
        elif self.tokenizer.tokenType() == "symbol" and self.tokenizer.current_token.value == '(':
            # Parenthesized expression
            self.output_file.write("<symbol> ( </symbol>\n")
            self.compileExpression()
            self.tokenizer.advance()
            self.output_file.write("<symbol> ) </symbol>\n")
        elif self.tokenizer.tokenType() == "symbol" and self.tokenizer.current_token.value in ['-', '~']:
            # Unary operation
            self.output_file.write(f"<symbol> {self.tokenizer.current_token.value} </symbol>\n")
            self.compileTerm()
        self.output_file.write("</term>\n")

    def compileExpressionList(self) -> int:
        """Parses an expression list."""
        num_Of_Expressions = 0
        while self.tokenizer.current_token.value != ")":
            self.compileExpression()
            num_Of_Expressions += 1
            if self.tokenizer.current_token.value == ",":
                self.tokenizer.advance()
        return num_Of_Expressions
