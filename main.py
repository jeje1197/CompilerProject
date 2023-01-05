# Imports
from lexer.lexer import Lexer
from parser.parser import Parser
from context.symbol_table import SymbolTable
from type_checker.type_checker import TypeChecker

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
    
    global_symbol_table = SymbolTable()
    global_symbol_table.set_local('true', 'int')
    global_symbol_table.set_local('false', 'int')
    global_symbol_table.set_local('null', 'void')

    type_checker = TypeChecker()
    try:
        type_checker.visit(ast, global_symbol_table)
    except Exception as e:
        print(e)
        continue

    print("Passed")

