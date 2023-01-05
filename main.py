# Imports
from lexer.lexer import Lexer
from parser.parser import Parser

while True:
    user_input = input('Ceroko>')

    if user_input.strip() == '-e':
        break

    # Lexing
    lexer = Lexer("Console", user_input)
    tokens = None
    try:
        tokens = lexer.get_tokens()
    except Exception as e:
        print(e)
        continue
    print(tokens)

    # Parsing
    parser = Parser(tokens)
    ast = None
    try:
        ast = parser.parse()
    except Exception as e:
        print(e)
        continue
    print(ast)



