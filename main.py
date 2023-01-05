# Imports
from lexer.lexer import Lexer
from parser.parser import Parser

# Main Code
lexer = Lexer("Console", "1++>=&&||2.8*4%()")
tokens = lexer.get_tokens()
print(tokens)

parser = Parser(tokens)
