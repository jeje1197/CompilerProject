# Imports
from lexer.lexer import Lexer
from parser.parser import Parser
from type_checker.type_checker import TypeChecker
from code_generator.code_gen import CodeGenerator

from os import path, mkdir

def run():
    while True:
        user_input = input('Ceroko>')
        command = user_input.strip()

        if user_input.strip() == '-e':
            break

        compile_sc('Console', user_input)

# def get_file_text(file_name):
def compile_sc(file_name, source_code):
    print('Parsing...')

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
    print('Validating program')
    type_checker = TypeChecker()
    try:
        type_checker.run(ast)
    except Exception as e:
        print(e)
        return

    # Code Generation
    print('Generating Code')
    code_generator = CodeGenerator()
    target_code = code_generator.generate_code()
    generate_file('test.spm', target_code)

def generate_file(file_name, target_code):
    output_dir = './output'
    if not path.exists(output_dir):
        mkdir(output_dir)

    output_file_path = f'{output_dir}/{file_name}'
    file = open(output_file_path, 'w')
    file.write(target_code)


if __name__ == '__main__':
    run()