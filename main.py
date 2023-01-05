# Imports
from lexer.lexer import Lexer
from parser.parser import Parser

while True:
    input = input('Ceroko>')

    lexer = Lexer("Console", "1++>=&&||2.8*4%()")
    tokens = lexer.get_tokens()
    print(tokens)

    parser = Parser(tokens)
    ast = parser.parse()

    print(ast)

