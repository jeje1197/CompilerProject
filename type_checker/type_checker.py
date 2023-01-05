from .type_system import TypeSystem

must_verify_sub_tree = ['VarDeclarationNode', 'FunctionDefNode', 'StructNode']
class TypeChecker:
    def __init__(self) -> None:
        self.type_system = TypeSystem()
    
    def visit(self, node, symbol_table):
        node_class = type(node).__name__
        if (type(node) is not list) and node.data_type and node_class not in must_verify_sub_tree:
            return node.data_type
        
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node, symbol_table)

    def visit_list(self, node, symbol_table):
        for statement_node in node:
            self.visit(statement_node, symbol_table)

    def visit_VarDeclarationNode(self, node, symbol_table):
        declared_type = node.data_type
        value_type = self.visit(node.node, symbol_table)

        if not self.type_system.type_matches(value_type, declared_type):
            raise Exception(f'Type mismatch {declared_type} <- {value_type} {node.position}')

        if symbol_table.contains_local(node.var_name):
            raise Exception(f'\'{node.var_name}\' is already in scope {node.position}')
        symbol_table.set_local(node.var_name, declared_type)

    def visit_VarAssignNode(self, node, symbol_table):
        if not symbol_table.contains_local(node.var_name):
            raise Exception(f'\'{node.var_name}\' has not been declared {node.position}')

        declared_type = symbol_table.get(node.var_name)
        value_type = self.visit(node.node, symbol_table)

        if not self.type_system.type_matches(value_type, declared_type):
            raise Exception(f'Type mismatch {declared_type} <- {value_type} {node.position}')

    def visit_VarAccessNode(self, node, symbol_table):
        if not symbol_table.contains_anywhere(node.var_name):
            raise Exception(f'\'{node.var_name}\' has not been declared {node.position}')
        return symbol_table.get(node.var_name)

    def visit_WhileNode(self, node, symbol_table):
        cond_node_type = self.visit(node.cond_node, symbol_table)
        if not self.type_system.type_matches(cond_node_type, 'int'):
            raise Exception(f'Type mismatch {cond_node_type} <- int {node.position}')


    def visit_FunctionCallNode(self, node, symbol_table):
        return self.visit(node.node_to_call, symbol_table)

    


        


    