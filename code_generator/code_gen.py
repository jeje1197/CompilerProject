from context.symbol_table import SymbolTable
from code_generator.operations import *
from code_generator.pre_written_mips.sub_routines import *
from type_checker.built_in_functions import * 


class CodeGenerator:
    def __init__(self) -> None:
        self.asm_data = ['.data'] # List of lines for data section
        self.asm_text = ['.text'] # List of lines for text section

        self.num_while = 0 # Number of while loops generated

    def generate_code(self, node):
        # Compiler Notes
        asm_code = "# MIPS assembly generated by the Ceroko Compiler\n\n"

        global_symbol_table = SymbolTable()
        add_function_def_to_symbol_table(global_symbol_table)
        
        global_symbol_table.begin_scope(self.asm_text)
        self.visit(node, global_symbol_table)
        global_symbol_table.end_scope(self.asm_text)

        # Terminate Program
        self.asm_text.append('li $v0, 10')
        self.asm_text.append('syscall')

        # Add prewritten subroutines

        # Combine .data and .text sections into one list
        self.asm_data.append('')
        self.asm_data.extend(self.asm_text)

        # Add .data and .text sections with code separated by newlines
        asm_code += '\n'.join(self.asm_data) + prewritten_mips
        return asm_code 

    def visit(self, node, symbol_table):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node, symbol_table)

    def visit_list(self, node, symbol_table):
        for statement_node in node:
            self.visit(statement_node, symbol_table)

    def visit_IntNode(self, node, symbol_table):
        gen_push_int(self.asm_text, node.value)

    def visit_CharNode(self, node, symbol_table):
        gen_push_int(self.asm_text, int(node.value))

    def visit_StringNode(self, node, symbol_table):
        gen_push_str(self.asm_data, node.value)

    def visit_UnaryOpNode(self, node, symbol_table):
        op = node.op
        metadata_obj = self.visit(node.node, symbol_table)
        expr_type = metadata_obj.get_sum_type()

    def visit_BinOpNode(self, node, symbol_table):
        self.visit(node.left_node, symbol_table)
        self.visit(node.right_node, symbol_table)
        op = node.op

        if op == '+':
            gen_add_int(self.asm_text)
        elif op == '-':
            gen_sub_int(self.asm_text)
        elif op == '*':
            gen_mul_int(self.asm_text)
        elif op == '/':
            gen_div_int(self.asm_text)
        elif op == '%':
            gen_mod_int(self.asm_text)
        elif op == '<':
            gen_lt_int(self.asm_text)
        elif op == '>':
            gen_gt_int(self.asm_text)
        elif op == '<=':
            gen_lte_int(self.asm_text)
        elif op == '>=':
            gen_gte_int(self.asm_text)
        elif op == '==':
            gen_ee_int(self.asm_text)
        elif op == '!=':
            gen_ne_int(self.asm_text)
        elif op == '&&':
            gen_and_int(self.asm_text)
        elif op == '||':
            gen_or_int(self.asm_text)
        

    def visit_TypeCastNode(self, node, symbol_table):
        pass

    def visit_VarDeclarationNode(self, node, symbol_table):
        # store value on top of stack
        self.visit(node.node, symbol_table)

        # store offset in symbol_table
        symbol_table.set_local(node.var_name, symbol_table.get_variable_offset())

    def visit_VarAssignNode(self, node, symbol_table):
        # get offset from symbol_table
        offset = symbol_table.get(node.name)

        # store value to stack
        self.visit(node.node, symbol_table)
        
        self.asm_text.extend([
            '# Reassign value to variable',
            'lw $a0, 0($sp)',
            'addiu $sp, $sp, 4',
            f'sw $a0, -{offset}($sp)',
            ''
        ])

    def visit_VarAccessNode(self, node, symbol_table):
        data = symbol_table.get(node.var_name)

        if type(data).__name__ == 'FunctionDefinition':
            function_def = data
            return function_def
        
        # get offset from symbol_table
        offset = symbol_table.get(node.var_name)

        self.asm_text.extend([
            '# Get variable from reference',
            f'lw $a0, -{offset}($fp)',
            'sw $a0, 0($sp)'
            'addiu $sp, $sp, -4',
            ''
        ])

    def visit_FunctionCallNode(self, node, symbol_table):
        function_def = self.visit(node.node_to_call, symbol_table)
        
        function_name = function_def.name
        if function_name == 'printi':
            gen_print_int(self.asm_text)
        elif function_name == 'printc':
            gen_print_char(self.asm_text)
        elif function_name == 'prints':
            gen_print_string(self.asm_text)
        