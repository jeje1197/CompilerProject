# Imports
from lexer.lexer import Lexer
from parser.parser import Parser
from context.symbol_table import SymbolTable
from type_checker.type_checker import TypeChecker

def run():
    while True:
        user_input = input('Ceroko>')
        command = user_input.strip()

        if user_input.strip() == '-e':
            break

        compile_sc('Console', user_input)

# def get_file_text(file_name):
def compile_sc(file_name, source_code):
    # Lexing
    lexer = Lexer(file_name, source_code)
    tokens = None
    try:
        tokens = lexer.get_tokens()
    except Exception as e:
        print(e)
        return
    print(tokens)

    # Parsing
    parser = Parser(tokens)
    ast = None
    try:
        ast = parser.parse()
    except Exception as e:
        print(e)
        return
    print(ast)
    
    # Type Checking
    type_checker = TypeChecker()
    type_checker.run(ast)

    print("Passed")

    # Code Generation

if __name__ == '__main__':
    run()