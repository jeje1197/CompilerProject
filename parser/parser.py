from .ast_node import *

class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.index = -1
        self.cur = None
        self.get_next()

    def has_next(self, steps_ahead=1):
        return self.index + steps_ahead < len(self.tokens)

    def get_next(self):
        if self.has_next():
            self.index += 1
            self.cur = self.tokens[self.index]
        else:
            self.cur = None
        return self.cur

    def look_ahead(self, steps_ahead=1):
        if self.has_next(steps_ahead):
            return self.tokens[self.index + steps_ahead]
        else:
            return None

    def skip_semicolons(self):
        while self.cur.matches('SEMICOLON'):
            self.get_next()

    def parse(self):
        """
        Returns an AST from a list of tokens
        """
        ast = self.statements('EOF')
        if not self.cur.matches('EOF'):
            raise Exception(f'Did not reach end of file {self.cur.position}')
        return ast

    def statements(self, end_type):
        statements_list = []

        self.skip_semicolons()
        while not self.cur.matches((end_type, 'EOF')):
            node = self.statement()

            if node:
                statements_list.append(node)
            else:
                break
            self.skip_semicolons()
        return statements_list

    def statement(self):
        if self.cur.matches('KEYWORD', 'var'):
            return self.var_declaration()
        elif self.cur.matches('ID') and self.look_ahead().matches('OP', '='):
            return self.var_assign()
        elif self.cur.matches('KEYWORD', 'if'):
            return self.if_statement()
        elif self.cur.matches('KEYWORD', 'while'):
            return self.while_loop()
        elif self.cur.matches('KEYWORD', 'break'):
            return self.break_statement()
        elif self.cur.matches('KEYWORD', 'continue'):
            return self.continue_statement()
        elif self.cur.matches('KEYWORD', 'fn'):
            return self.function_def()
        elif self.cur.matches('KEYWORD', 'return'):
            return self.return_statement()
        elif self.cur.matches('KEYWORD', 'struct'):
            return self.struct_def()
        
        return self.expr()

    def read_type(self):
        type_str = ""
        if not self.cur.matches('ID'):
            return None
        type_str += self.cur.value
        self.get_next()

        while self.cur.matches('DOT') and self.look_ahead().matches('ID'):
            self.get_next()
            type_str += self.cur.value
            self.get_next()

        while self.cur.matches('OP', '*'):
            type_str += self.cur.value
            self.get_next()
        return type_str

    def var_declaration(self):
        if not self.cur.matches('KEYWORD', 'var'):
            raise Exception(f'Expected keyword \'var\' {self.cur.position}')
        start_pos = self.cur.position
        self.get_next()

        if not self.cur.matches('ID'):
            raise Exception(f'Expected identifier name {self.cur.position}')
        var_name = self.cur.value
        self.get_next()

        if not self.cur.matches('COLON'):
            raise Exception(f'Expected \':\' {self.cur.position}')
        self.get_next()

        type_name = self.read_type()
        if not type_name:
            raise Exception(f'Expected type name {self.cur.position}')
        
        if not self.cur.matches('OP', '='):
            raise Exception(f'Expected \'=\' {self.cur.position}')
        self.get_next()

        value_node = self.expr()
        if not value_node:
            raise Exception(f'Expected expression after \'=\' {self.cur.position}')
        return VarDeclarationNode(type_name, var_name, value_node, start_pos)

    def var_assign(self):
        if not self.cur.matches('ID'):
            raise Exception(f'Expected identifier name {self.cur.position}')
        start_pos = self.cur.position
        var_name = self.cur.value
        self.get_next()

        if not self.cur.matches('OP', '='):
            raise Exception(f'Expected \'=\' {self.cur.position}')
        self.get_next()

        value_node = self.expr()
        if not value_node:
            raise Exception(f'Expected expression after \'=\' {self.cur.position}')
        return VarAssignNode(var_name, value_node, start_pos)

    def type_cast(self):
        start_pos = self.cur.position
        self.get_next()

        if not self.cur.matches('COLON'):
            raise Exception(f'Expected \':\' {self.cur.position}')
        self.get_next()

        type_name = self.read_type()
        if not type_name:
            raise Exception(f'Expected type name {self.cur.position}')
        
        node = self.expr()
        if not node:
            raise Exception(f'Expected expression after \'=\' {self.cur.position}')
        return TypeCastNode(node, type_name, start_pos)

    def if_statement(self):
        start_pos = self.cur.position
        self.get_next()

        case_tuples = []
        else_statements = None
        if not self.cur.matches('LPAREN'):
            raise Exception(f'Expected ( {self.cur.position}')
        self.get_next()

        cond_node = self.expr()
        if not cond_node:
            raise Exception(f'Expected expression after \'(\' {self.cur.position}')

        if not self.cur.matches('RPAREN'):
            raise Exception(f'Expected ) {self.cur.position}')
        self.get_next()

        if not self.cur.matches('LBRACE'):
            raise Exception(f'Expected {"{"} at {self.cur.position}')
        self.get_next()

        statements = self.statements('RBRACE')

        if not self.cur.matches('RBRACE'):
            raise Exception(f'Expected {"}"} {self.cur.position}')
        self.get_next()
        case_tuple = (cond_node, statements)
        case_tuples.append(case_tuple)

        while self.cur.matches('else if'):
            if not self.cur.matches('LPAREN'):
                raise Exception(f'Expected ( {self.cur.position}')
            self.get_next()

            cond_node = self.expr()
            if not cond_node:
                raise Exception(f'Expected expression after \'(\' {self.cur.position}')

            if not self.cur.matches('RPAREN'):
                raise Exception(f'Expected ) {self.cur.position}')
            self.get_next()

            if not self.cur.matches('LBRACE'):
                raise Exception(f'Expected {"{"} {self.cur.position}')
            self.get_next()

            statements = self.statements('RBRACE')

            if not self.cur.matches('RBRACE'):
                raise Exception(f'Expected {"}"} {self.cur.position}')
            self.get_next()
            case_tuple = (cond_node, statements)
            case_tuples.append(case_tuple)

        if self.cur.matches('else'):
            self.get_next()

            if not self.cur.matches('LBRACE'):
                raise Exception(f'Expected {"{"} {self.cur.position}')
            self.get_next()

            else_statements = self.statements('RBRACE')

            if not self.cur.matches('RBRACE'):
                raise Exception(f'Expected {"}"} {self.cur.position}')
            self.get_next()
        return IfNode(case_tuples, else_statements, start_pos)

    def while_loop(self):
        start_pos = self.cur.position
        self.get_next()

        if not self.cur.matches('LPAREN'):
            raise Exception(f'Expected ( {self.cur.position}')
        self.get_next()

        cond_node = self.expr()
        if not cond_node:
            raise Exception(f'Expected expression after \'(\' {self.cur.position}')

        if not self.cur.matches('RPAREN'):
            raise Exception(f'Expected ) {self.cur.position}')
        self.get_next()

        if not self.cur.matches('LBRACE'):
            raise Exception(f'Expected {"{"} {self.cur.position}')
        self.get_next()

        statements = self.statements('RBRACE')

        if not self.cur.matches('RBRACE'):
            raise Exception(f'Expected {"}"} {self.cur.position}')
        self.get_next()
        return WhileNode(cond_node, statements, start_pos)

    def break_statement(self):
        start_pos = self.cur.position
        self.get_next()
        return BreakNode(start_pos)

    def continue_statement(self):
        start_pos = self.cur.position
        self.get_next()
        return ContinueNode(start_pos)

    def function_def(self):
        start_pos = self.cur.position
        self.get_next()

        if not self.cur.matches('ID'):
            raise Exception(f'Expected function name {self.cur.position}')
        fn_name = self.cur.value
        self.get_next()

        if not self.cur.matches('LPAREN'):
            raise Exception(f'Expected ( {self.cur.position}')
        self.get_next()

        args_w_types = []

        if self.cur.matches('ID'):
            var_name = self.cur.value
            self.get_next()

            if not self.cur.matches('COLON'):
                raise Exception(f'Expected \':\' {self.cur.position}')
            self.get_next()

            type_name = self.read_type()
            if not type_name:
                raise Exception(f'Expected type name {self.cur.position}')
            arg_tuple = (var_name, type_name)
            args_w_types.append(arg_tuple)
        
            while self.cur.matches('COMMA'):
                self.get_next()

                if self.cur.matches('ID'):
                    var_name = self.cur.value
                    self.get_next()

                    if not self.cur.matches('COLON'):
                        raise Exception(f'Expected \':\' {self.cur.position}')
                    self.get_next()

                    type_name = self.read_type()
                    if not type_name:
                        raise Exception(f'Expected type name {self.cur.position}')
                    arg_tuple = (var_name, type_name)
                    args_w_types.append(arg_tuple)

        if not self.cur.matches('RPAREN'):
            raise Exception(f'Expected closing \')\' {self.cur.position}')    
        self.get_next()

        if not self.cur.matches('COLON'):
            raise Exception(f'Expected \':\' {self.cur.position}')
        self.get_next()

        return_type = self.read_type()
        if not return_type:
            raise Exception(f'Expected type name {self.cur.position}')

        if not self.cur.matches('LBRACE'):
            raise Exception(f'Expected {"{"} {self.cur.position}')
        self.get_next()

        statements = self.statements('RBRACE')

        if not self.cur.matches('RBRACE'):
            print(self.cur)
            raise Exception(f'Expected {"}"} {self.cur.position}')
        self.get_next()
        return FunctionDefNode(fn_name,  args_w_types, return_type, statements, start_pos)


    def return_statement(self):
        start_pos = self.cur.position
        self.get_next()

        value_node = self.expr()
        return ReturnNode(value_node, start_pos)


    def struct_def(self):
        start_pos = self.cur.position
        self.get_next()

        if not self.cur.matches('ID'):
            raise Exception(f'Expected struct name  {self.cur.position}')
        struct_name = self.cur.value
        self.get_next()

        if not self.cur.matches('LBRACE'):
            raise Exception(f'Expected {"{"} {self.cur.position}')
        self.get_next()

        statements = self.statements('RBRACE')

        if not self.cur.matches('RBRACE'):
            raise Exception(f'Expected {"}"} {self.cur.position}')
        self.get_next()
        return StructNode(struct_name, statements, start_pos)

    def expr(self):
        return self.bin_op(self.comp_expr, ('&&', '||'), self.comp_expr)

    def comp_expr(self):
        return self.bin_op(self.comp_expr2, ('<', '>', '<=', '>=', '==', '!=', '%'), self.comp_expr2)

    def comp_expr2(self):
        return self.bin_op(self.term, ('+', '-'), self.term)

    def term(self):
        return self.bin_op(self.power, ('*', '/', '%'), self.power)

    def power(self):
        return self.bin_op(self.modifier, ('^'), self.power)

    def modifier(self):
        atom_node = self.atom()

        while atom_node and self.cur.matches(('LPAREN', 'DOT', 'RBRACKET')):
            atom_node = self.function_call(atom_node)
            atom_node = self.attribute_access(atom_node)
            atom_node = self.index_access(atom_node)
        return atom_node

    def function_call(self, atom_node):
        if not self.cur.matches('LPAREN'):
            return atom_node
        self.get_next()

        args = []
        expr_node = self.expr()
        if expr_node:
            args.append(expr_node)
            while expr_node and self.cur.matches('COMMA'):
                self.get_next()

                expr_node = self.expr()
                if expr_node:
                    args.append(expr_node)

        if not self.cur.matches('RPAREN'):
            raise Exception(f'Expected closing \')\' {self.cur.position}')    
        self.get_next()
        return FunctionCallNode(atom_node, args, atom_node.position)

    def index_access(self, atom_node):
        if not self.cur.matches('LBRACKET'):
            return atom_node
        start_pos = self.cur.position
        self.get_next()

        index_node = self.expr()
        if not index_node:
            raise Exception('Expected index')
        
        if not self.cur.matches('RBRACKET'):
            raise Exception(f'Expected \']\' {self.cur.position}')
        return IndexAccessNode(atom_node, index_node, start_pos)

    def attribute_access(self, atom_node):
        if not self.cur.matches('DOT'):
            return atom_node
        self.get_next()

        if not self.cur.matches('ID'):
            raise Exception(f'Expected attribute name {self.cur.position}')
        attribute_name = self.cur.value
        self.get_next()
        return AttributeAccessNode(atom_node, attribute_name, atom_node.position)
    
    def atom(self):
        tok = self.cur
        
        if tok.type == 'OP' and tok.value in ('+', '-', '!', '*', '&'): # UnaryOp
            self.get_next()

            node = self.expr()
            if not node:
                raise Exception(f'Expected expression after \'{tok.value}\' {self.cur.position}')
            return UnaryOpNode(tok.value, node, tok.position)
        elif tok.matches('KEYWORD', 'cast'):
            return self.type_cast()
        elif tok.matches('INT'): # Integer
            self.get_next()
            return IntNode(tok.value, tok.position)
        elif tok.matches('FLOAT'): # Float
            self.get_next()
            return FloatNode(tok.value, tok.position)
        elif tok.matches('CHAR'): # Char
            self.get_next()
            return CharNode(tok.value, tok.position)
        elif tok.matches('STRING'): # String
            self.get_next()
            return StringNode(tok.value, tok.position)
        elif tok.matches('ID'): # Variable Access
            self.get_next()
            return VarAccessNode(tok.value, tok.position)
        elif tok.matches('LPAREN'): # Parenthesis
            self.get_next()
            
            expr_node = self.expr()
            if not expr_node:
                raise Exception(f'Expected expression after \'{tok.value}\' {self.cur.position}')

            if not self.cur.matches('RPAREN'):
                raise Exception(f'Unclosed Parenthesis {self.cur.position}')
            self.get_next()
            return expr_node
        elif tok.matches('LBRACKET'):
            array = []
            self.get_next()

            expr_node = self.expr()
            if expr_node:
                array.append(expr_node)
            while expr_node and self.cur.matches('COMMA'):
                self.get_next()

                expr_node = self.expr()
                if expr_node:
                    array.append(expr_node)
            
            return ArrayNode(array, tok.position)
        return None            

    def bin_op(self, func_1, ops, func_2):
        left_node = func_1()

        while self.cur.matches('OP', ops):
            op_tok = self.cur
            self.get_next()

            right_node = func_2()
            if not right_node:
                raise Exception(f'Expected expression after {op_tok.value} {op_tok.position}')
            left_node = BinOpNode(left_node, op_tok.value, right_node, left_node.position)
        return left_node
