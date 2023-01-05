from .type_system import TypeSystem

class TypeChecker:
    def __init__(self) -> None:
        self.type_system = TypeSystem()
    
    def visit(self, node, symbol_table):
        if node.data_type:
            return node.data_type
        method_name = f'visit_{type(node).__class__}'
        method = getattr(self, method_name)
        return method(node, symbol_table)

    def visit_VarDeclarationNode(self, node, symbol_table):
        declared_type = node.type
        value_type = self.visit(node.node, symbol_table)

        if not self.type_system.type_matches(declared_type, value_type):
            raise Exception(f'Type mismatch {declared_type} <- {value_type} {node.position}')

        if symbol_table.contains_local(node.var_name):
            raise Exception(f'\'{node.var_name}\' is already in scope {node.position}')
        symbol_table.set_local(node.var_name, declared_type)

    def visit_VarAssignNode(self, node, symbol_table):
        if not symbol_table.contains_local(node.var_name):
            raise Exception(f'\'{node.var_name}\' has not been declared {node.position}')

        declared_type = symbol_table.get(node.var_name)
        value_type = self.visit(node.node, symbol_table)

        if not self.type_system.type_matches(declared_type, value_type):
            raise Exception(f'Type mismatch {declared_type} <- {value_type} {node.position}')

    def visit_VarAccessNode(self, node, symbol_table):
        if not symbol_table.contains_local(node.var_name):
            raise Exception(f'\'{node.var_name}\' has not been declared {node.position}')
        return symbol_table.get(node.var_name)

    


        


    