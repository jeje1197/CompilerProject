from .type_system import TypeSystem
from .metadata import Metadata, FunctionDefinition, StructDefinition

must_verify_sub_tree = ['VarDeclarationNode', 'TypeCastNode', 'FunctionDefNode', 'StructNode']
class TypeChecker:
    def __init__(self) -> None:
        self.type_system = TypeSystem()
    
    def visit(self, node, symbol_table):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node, symbol_table)

    def visit_list(self, node, symbol_table):
        for statement_node in node:
            self.visit(statement_node, symbol_table)

    def visit_IntNode(self, node, symbol_table):
        return Metadata('int', None)

    def visit_FloatNode(self, node, symbol_table):
        return Metadata('float', None)

    def visit_CharNode(self, node, symbol_table):
        return Metadata('char', None)

    def visit_StringNode(self, node, symbol_table):
        return Metadata('char*', None)

    def visit_UnaryOpNode(self, node, symbol_table):
        op = node.op
        expr_type = self.visit(node.node, symbol_table)
        result_type = None

        # if op == '+':
        #     'int' * expr_type
        # elif op == '-':
        #     'int' * expr_type
        # elif op == '!':
        #     'int'
        # elif op == '*':
        #     expr_type
        # elif op == '&':

        return result_type

    def visit_BinOpNode(self, node, symbol_table):
        left_type = self.visit(node.left_node, symbol_table)
        op = node.op
        right_type = self.visit(node.right_node, symbol_table)

        return
            
    def visit_TypeCastNode(self, node, symbol_table):
        original_metadata_obj = self.visit(node.node, symbol_table)
        original_type = original_metadata_obj.get_sum_type()
        desired_type = node.data_type

        if not self.type_system.type_castable(original_type, desired_type):
            raise Exception(f'Type {original_type} cannot be casted to {desired_type} {node.position}')
        
        return Metadata(desired_type, original_metadata_obj.get_metadata())

    def visit_VarDeclarationNode(self, node, symbol_table):
        declared_type = node.data_type
        metadata_obj = self.visit(node.node, symbol_table)
        value_type = metadata_obj.get_sum_type()

        if symbol_table.contains_local(node.var_name):
            raise Exception(f'\'{node.var_name}\' is already in scope {node.position}')

        if not self.type_system.type_matches(value_type, declared_type):
            raise Exception(f'Type mismatch {declared_type} <- {value_type} {node.position}')
        
        metadata = Metadata(declared_type, metadata_obj.get_metadata())
        symbol_table.set_local(node.var_name, metadata)

    def visit_VarAssignNode(self, node, symbol_table):
        if not symbol_table.contains_local(node.var_name):
            raise Exception(f'\'{node.var_name}\' has not been declared {node.position}')

        declared_type = symbol_table.get(node.var_name).get_sum_type()
        metadata_obj = self.visit(node.node, symbol_table)
        value_type = metadata_obj.get_sum_type()

        if not self.type_system.type_matches(value_type, declared_type):
            raise Exception(f'Type mismatch {declared_type} <- {value_type} {node.position}')
        
        new_metadata_obj = Metadata(declared_type, metadata_obj.get_metadata())
        symbol_table.set_in_lowest_scope(node.var_name, new_metadata_obj)

    def visit_VarAccessNode(self, node, symbol_table):
        if not symbol_table.contains_anywhere(node.var_name):
            raise Exception(f'\'{node.var_name}\' has not been declared {node.position}')
        return symbol_table.get(node.var_name)

    def visit_WhileNode(self, node, symbol_table):
        cond_node_type = self.visit(node.cond_node, symbol_table)[0]
        if not self.type_system.type_matches(cond_node_type, 'int'):
            raise Exception(f'Type mismatch {cond_node_type} <- int {node.position}')
        propagated_type = self.visit(node.statements)
        node.data_type = propagated_type

    def visit_BreakNode(self, node, symbol_table):
        return ('void', node)

    def visit_ContinueNode(self, node, symbol_table):
        return ('void', node)

    def visit_FunctionDefNode(self, node, symbol_table):
        if symbol_table.contains_local(node.name):
            raise Exception(f'\'{node.name}\' is already in scope {node.position}')

        if not self.type_system.is_valid_type(node.return_type):
                raise Exception(f'Invalid return type \'{node.return_type}\' for function \'{node.name}\' {node.position}')
        
        fn_symbol_table = symbol_table.generate_sub_context()
        arg_names_seen = set()
        for arg in node.args_w_types:
            if arg[0] in arg_names_seen:
                raise Exception('')
            else:
                arg_names_seen.add(arg[0])

            if not self.type_system.is_valid_type(arg[1]):
                raise Exception(f'Invalid type \'{arg[1]}\' for argument \'{arg[0]}\' {node.position}')
            
            fn_symbol_table.set_local(arg[0], (arg[1], None))

        for statement in node.statements:
            self.visit(statement, fn_symbol_table)

        return (node.return_type, node)

    def visit_ReturnNode(self, node, symbol_table):
        return (self.visit(node.node, symbol_table)[0] if node.node else 'void', node.node)


    def visit_FunctionCallNode(self, node, symbol_table):
        return self.visit(node.node_to_call, symbol_table)

    


        


    