from ast_node import *

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
        while self.cur and self.cur.matches('SEMICOLON'):
            self.get_next()

    def parse(self):
        """
        Returns an AST from a list of tokens
        """
        ast = self.statements()

        if not self.cur.matches('EOF'):
            raise Exception('Did not reach end of file')
        return ast

    def statements(self, end_type):
        statements_list = []

        self.skip_semicolons()
        while self.cur and not self.matches((end_type, 'EOF')):
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
        elif self.cur.matches('KEYWORD', 'fn'):
            return self.function_def()
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
        start_pos = self.cur.position
        self.get_next()

        if not self.cur.matches('ID'):
            raise Exception('Expected identifier name')
        var_name = self.cur.value
        self.get_next()

        if not self.cur.matches('COLON'):
            raise Exception('Expected \':\'')
        self.get_next()

        type_name = self.read_type()
        if not type_name:
            raise Exception('Expected type name')
        
        if not self.cur.matches('OP', '='):
            raise Exception('Expected \'=\'')
        self.get_next()

        value_node = self.expr()
        if not value_node:
            raise Exception('Expected expression after \'=\'')
        return VarDeclarationNode(type_name, var_name, value_node, start_pos)

    def var_assign(self):
        if not self.cur.matches('ID'):
            raise Exception('Expected identifier name')
        start_pos = self.cur.position
        var_name = self.cur.value
        self.get_next()

        if not self.cur.matches('OP', '='):
            raise Exception('Expected \'=\'')
        self.get_next()

        value_node = self.expr()
        if not value_node:
            raise Exception('Expected expression after \'=\'')
        return VarAssignNode(var_name, value_node, start_pos)

    def if_statement():
        pass

    def while_loop():
        pass

    def function_def():
        pass

    def struct_def():
        pass

    def expr(self):
        return self.comp_expr()

    def comp_expr(self):
        return self.bin_op(self.comp_expr2, ('&&', '||'), self.comp_expr2)

    def comp_expr2(self):
        return self.bin_op(self.term, ('<', '>', '<=', '>=', '==', '!=', '%'), self.term)

    def term(self):
        return self.bin_op(self.power, ('*', '/', '%'), self.power)

    def power(self):
        return self.bin_op(self.modifier, ('^'), self.power)

    def modifier(self):
        atom_node = self.atom()

        while atom_node and self.cur.matches(('(', '.', '[')):
            atom_node = self.function_call(atom_node)
            atom_node = self.attribute_access(atom_node)
            atom_node = self.index_access(atom_node)

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
            raise Exception('Expected closing \')\'')    
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
            raise Exception('Expected \']\'')
        return IndexAccessNode(atom_node, index_node, start_pos)

    def attribute_access(self, atom_node):
        if not self.cur.matches('DOT'):
            return atom_node
        self.get_next()

        if not self.cur.matches('ID'):
            raise Exception('Expected attribute name')
        attribute_name = self.cur.value
        self.get_next()
        return AttributeAccessNode(atom_node, attribute_name, atom_node.position)
    
    def atom(self):
        tok = self.cur
        
        if tok.type == 'OP' and tok.value in ('+', '-', '!', '*', '&'): # UnaryOp
            self.get_next()

            node = self.expr()
            if not node:
                raise Exception(f'Expected expression after \'{tok.value}\'')
            return UnaryOpNode(tok.value, node, tok.position)
        elif tok.matches('INT'): # Integer
            self.get_next()
            return IntNode(tok.value, tok.position)
        elif tok.matches('FLOAT'): # Float
            self.get_next()
            return FloatNode(tok.value, tok.position)
        elif tok.matches('STRING'): # String
            self.get_next()
            return StringNode(tok.value, tok.position)
        elif tok.matches('ID'): # Variable Access
            self.get_next()
            return VarAccessNode(tok.value, tok.position)
        elif tok.matches('LPAREN'): # Parenthesis
            self.get_next()
            
            expr_node = self.expr()
            if not node:
                raise Exception(f'Expected expression after \'{tok.value}\'')

            if not self.cur.matches('RPAREN'):
                raise Exception('Unclosed Parenthesis')
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

        while self.cur and self.cur in ops:
            op_tok = self.cur
            self.get_next()

            right_node = func_2()
            left_node = BinOpNode(left_node, op_tok.value, right_node)
        return left_node
