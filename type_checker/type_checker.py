from .type_system import TypeSystem
from .metadata import Metadata, FunctionDefinition, StructDefinition
from context.symbol_table import SymbolTable

must_verify_sub_tree = ['VarDeclarationNode', 'TypeCastNode', 'FunctionDefNode', 'StructNode']
class TypeChecker:
    def __init__(self) -> None:
        self.type_system = TypeSystem()

    def run(self, ast:list):
        global_symbol_table = SymbolTable()
        global_symbol_table.set_local('true', Metadata('int', None))
        global_symbol_table.set_local('false', Metadata('int', None))
        global_symbol_table.set_local('null', Metadata('void*', None))
        self.visit(ast, global_symbol_table)
    
    def visit(self, node, symbol_table):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node, symbol_table)

    def visit_list(self, node, symbol_table):
        metadata_list = []
        for statement_node in node:
            metadata_obj = self.visit(statement_node, symbol_table)
            if type(statement_node).__name__ in ('IfNode', 'WhileNode', 'ReturnNode'):
                metadata_list.append(metadata_obj)
        return metadata_list

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
        metadata_obj = self.visit(node.node, symbol_table)
        expr_type = metadata_obj.get_sum_type()

        result_type = self.type_system.get_type_from_unary_op(expr_type, op)
        if not result_type:
            raise Exception(f'Invalid operation between types: {op} {expr_type} {node.position}')
        return Metadata(result_type, None)

    def visit_BinOpNode(self, node, symbol_table):
        left_metadata_obj = self.visit(node.left_node, symbol_table)
        op = node.op
        right_metadata_obj = self.visit(node.right_node, symbol_table)

        left_type = left_metadata_obj.get_sum_type()
        right_type = right_metadata_obj.get_sum_type()

        result_type = self.type_system.get_type_from_bin_op(left_type, op, right_type)
        if not result_type:
            raise Exception(f'Invalid operation between types: {left_type} {op} {right_type} {node.position}')
        return Metadata(result_type, None)
            
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
        return metadata

    def visit_VarAssignNode(self, node, symbol_table):
        if not symbol_table.contains_anywhere(node.var_name):
            raise Exception(f'\'{node.var_name}\' has not been declared {node.position}')

        declared_type = symbol_table.get(node.var_name).get_sum_type()
        metadata_obj = self.visit(node.node, symbol_table)
        value_type = metadata_obj.get_sum_type()

        if not self.type_system.type_matches(value_type, declared_type):
            raise Exception(f'Type mismatch {declared_type} <- {value_type} {node.position}')
        
        new_metadata_obj = Metadata(declared_type, metadata_obj.get_metadata())
        symbol_table.set_in_lowest_scope(node.var_name, new_metadata_obj)
        return new_metadata_obj

    def visit_VarAccessNode(self, node, symbol_table):
        if not symbol_table.contains_anywhere(node.var_name):
            raise Exception(f'\'{node.var_name}\' has not been declared {node.position}')
        return symbol_table.get(node.var_name)

    def visit_IfNode(self, node, symbol_table):
        return_type = None
        for case in node.case_tuples:
            cond_metadata_obj = self.visit(case[0], symbol_table)
            cond_node_type = cond_metadata_obj.get_sum_type()
            if not self.type_system.type_matches(cond_node_type, 'int'):
                raise Exception(f'Type mismatch int <- {cond_node_type} in if statement condition {node.position}')
            
            metadata_objs = self.visit(case[1], symbol_table)
            for metadata_obj in metadata_objs:
                sum_type = metadata_obj.get_sum_type()
                if sum_type is not None:
                    if return_type and not self.type_system.type_matches(return_type, sum_type):
                        raise Exception(f'Conflicting return types found in while loop {node.position}')
                    return_type = sum_type
        return Metadata(return_type, None)

    def visit_WhileNode(self, node, symbol_table):
        cond_metadata = self.visit(node.cond_node, symbol_table)
        cond_node_type = cond_metadata.get_sum_type()
        if not self.type_system.type_matches(cond_node_type, 'int'):
            raise Exception(f'Type mismatch int <- {cond_node_type} {node.position}')
        metadata_objs = self.visit(node.statements, symbol_table)

        return_type = None
        for metadata_obj in metadata_objs:
            sum_type = metadata_obj.get_sum_type()
            if sum_type is not None:
                if return_type and not self.type_system.type_matches(return_type, sum_type):
                    raise Exception(f'Conflicting return types found in while loop {node.position}')
                return_type = sum_type
        return Metadata(return_type, None)

    def visit_BreakNode(self, node, symbol_table):
        return Metadata(None, None)

    def visit_ContinueNode(self, node, symbol_table):
        return Metadata(None, None)

    def visit_FunctionDefNode(self, node, symbol_table):
        if symbol_table.contains_local(node.name):
            raise Exception(f'\'{node.name}\' is already in scope {node.position}')
        function_def = FunctionDefinition(node.name, node.args_w_types, node.return_type)
        function_metadata_obj = Metadata('fn', function_def)
        symbol_table.set_local(node.name, function_metadata_obj)

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

        declared_type = node.data_type
        metadata_objs = self.visit(node.statements, symbol_table)
        for metadata_obj in metadata_objs:
            metadata_type = metadata_obj.get_sum_type()
            if not self.type_system.type_matches(metadata_type, declared_type):
                raise Exception(f'Invalid return type {metadata_type} found in function \'{node.name}\': {declared_type} at {node.position}')
        return function_metadata_obj

    # If a return statement is called with no value, declare its type as 'void'
    # Otherwise substructures without a return statement have a type of None
    def visit_ReturnNode(self, node, symbol_table):
        if node.node:
            return self.visit(node.node, symbol_table)
        return Metadata('void', None)

    def visit_FunctionCallNode(self, node, symbol_table):
        metadata_obj = self.visit(node.node_to_call, symbol_table)
        function_def = metadata_obj.get_metadata()
        if not type(function_def).__name__ == 'FunctionDefinition':
            raise Exception(f'{metadata_obj.get_sum_type()} is not callable {node.position}')

        num_passed = len(node.args)
        num_expected = len(function_def.args_w_types)
        if not num_passed == num_expected:
            raise Exception(f'Function \'{function_def.name}\' expected {num_expected} args, but received {num_passed} {node.position}')

        for i in range(num_expected):
            arg_type = self.visit(node.args[i]).get_sum_type()
            expected_type = function_def.args_w_types[i][1]
            if not self.type_system.type_matches(arg_type, expected_type):
                raise Exception(f'Type mismatch arg{i} in \'{function_def.name}\': {expected_type} <- {arg_type} {node.position}')
        return Metadata(function_def.return_type, None)

    def visit_StructNode(self, node, symbol_table):
        if symbol_table.contains_local(node.name):
            raise Exception(f'\'{node.name}\' is already in scope {node.position}')
        struct_def = StructDefinition(node.name)
        struct_metadata_obj = Metadata(node.name, struct_def)
        symbol_table.set_local(node.name, struct_metadata_obj)

        for statement in node.statements:
            if type(statement).__name__ == 'VarDeclarationNode':
                metadata_obj = self.visit(statement, symbol_table)
                field_name = statement.var_name
                if not struct_def.add_field(field_name, metadata_obj):
                    raise Exception(f'Structure already contains a \'{field_name}\' field {statement.position}')
            else:
                raise Exception(f'{type(statement).__name__} cannot exist within a structure {statement.position}')
        return Metadata(node.name, struct_def)
        
    def visit_AttributeAccessNode(self, node, symbol_table):
        struct_metadata_obj = self.visit(node.node, symbol_table)
        struct_def = struct_metadata_obj.get_metadata()
        if not type(struct_def).__name__ == 'StructDefinition':
            raise Exception(f'{struct_metadata_obj.get_sum_type()} is not a structure {node.position}')

        attribute_metadata_obj = struct_def.get_field(node.attribute_name)
        if not attribute_metadata_obj:
            raise Exception(f'\'{node.attribute_name}\' does not belong to struct \'{struct_def.name}\' {node.position}')
        return attribute_metadata_obj

    def visit_AttributeAssignNode(self, node, symbol_table):
        struct_metadata_obj = self.visit(node.node, symbol_table)
        struct_def = struct_metadata_obj.get_metadata()
        if not type(struct_def).__name__ == 'StructDefinition':
            raise Exception(f'{struct_metadata_obj.get_sum_type()} is not a structure {node.position}')
        
        attribute_metadata_obj = struct_def.get_field(node.attribute_name)
        attribute_type = attribute_metadata_obj.get_sum_type()
        if not attribute_metadata_obj:
            raise Exception(f'\'{node.attribute_name}\' does not belong to struct \'{struct_def.name}\' {node.position}')

        value_metadata_obj = self.visit(node.value_node, symbol_table)
        value_type = value_metadata_obj.get_sum_type()
        if not self.type_system.type_matches(value_type, attribute_type):
            raise Exception(f'Type mismatch {struct_def.name}.{node.attribute_name}: {attribute_type} <- {value_type} {node.position}')

        new_metadata_obj = Metadata(attribute_type, value_metadata_obj.get_metadata())
        struct_def.set_field(node.attribute_name, new_metadata_obj)
        return new_metadata_obj

    def visit_IndexAccessNode(self, node, symbol_table):
        array_metadata_obj = self.visit(node.node, symbol_table)
        pointer_type = array_metadata_obj.get_sum_type()
        if not self.type_system.is_pointer_type(pointer_type):
            raise Exception(f'Type {pointer_type} is not indexable {node.position}')
        
        array_element_type = self.type_system.dereference_pointer_type(pointer_type)
        return Metadata(array_element_type, None)
