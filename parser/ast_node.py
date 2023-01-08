class AstNode:
    def __init__(self, is_expr=False, data_type=None):
        self.is_expr = is_expr
        self.data_type = data_type
        self.cast_info = [None, None]

    def __repr__(self) -> str:
        return f'(AstNode {type(self).__name__}: is_expr: {self.is_expr} data_type: {self.data_type}'


class UnaryOpNode(AstNode):
    def __init__(self, op, node, position) -> None:
        super().__init__(True, None)
        self.op = op
        self.node = node
        self.position = position


class BinOpNode(AstNode):
    def __init__(self, left_node, op, right_node, position) -> None:
        super().__init__(True, None)
        self.left_node = left_node
        self.op = op
        self.right_node = right_node
        self.position = position

class TypeCastNode(AstNode):
    def __init__(self, node, type, position) -> None:
        super().__init__(True, type)
        self.node = node
        self.position = position


class IntNode(AstNode):
    def __init__(self, value, position) -> None:
        super().__init__(True, 'int')
        self.value = value
        self.position = position


class FloatNode(AstNode):
    def __init__(self, value, position) -> None:
        super().__init__(True, 'float')
        self.value = value
        self.position = position


class CharNode(AstNode):
    def __init__(self, value, position) -> None:
        super().__init__(True, 'char')
        self.value = value
        self.position = position


class StringNode(AstNode):
    def __init__(self, value, position) -> None:
        super().__init__(True, 'char*')
        self.value = value
        self.position = position


class VarDeclarationNode(AstNode):
    def __init__(self, type, var_name, node, position) -> None:
        super().__init__(True, type)
        self.var_name = var_name
        self.node = node
        self.position = position


class VarAssignNode(AstNode):
    def __init__(self, var_name, node, position) -> None:
        super().__init__(True, None)
        self.var_name = var_name
        self.node = node
        self.position = position


class VarAccessNode(AstNode):
    def __init__(self, var_name, position) -> None:
        super().__init__(True, None)
        self.var_name = var_name
        self.position = position


class IfNode(AstNode):
    def __init__(self, case_tuples, else_statements, position) -> None:
        super().__init__(True, None)
        self.case_tuples = case_tuples
        self.else_statements = else_statements
        self.position = position


class WhileNode(AstNode):
    def __init__(self, cond_node, statements, position) -> None:
        super().__init__(True, None)
        self.cond_node = cond_node
        self.statements = statements
        self.position = position


class BreakNode(AstNode):
    def __init__(self, position):
        super().__init__(False, None)
        self.position = position


class ContinueNode(AstNode):
    def __init__(self, position):
        super().__init__(False, None)
        self.position = position


class FunctionDefNode(AstNode):
    def __init__(self, name, args_w_types, return_type, statements, position) -> None:
        super().__init__(True, return_type)
        self.name = name
        self.args_w_types = args_w_types
        self.return_type = return_type
        self.statements = statements
        self.position = position


class FunctionCallNode(AstNode):
    def __init__(self, node_to_call, args, position) -> None:
        super().__init__(True, None)
        self.node_to_call = node_to_call
        self.args = args
        self.position = position


class ReturnNode(AstNode):
    def __init__(self, node, position):
        super().__init__(False, None)
        self.node = node
        self.position = position


class ArrayNode(AstNode):
    def __init__(self, elements, position) -> None:
        super().__init__(True, None)
        self.elements = elements
        self.position = position

class IndexAccessNode(AstNode):
    def __init__(self, node, index_node, position) -> None:
        super().__init__(True, None)
        self.node = node
        self.index_node = index_node
        self.position = position


class StructNode(AstNode):
    def __init__(self, name, statements, position) -> None:
        super().__init__(True, None)
        self.name = name
        self.statements = statements
        self.position = position


class AttributeAccessNode(AstNode):
    def __init__(self, node, attribute_name, position) -> None:
        super().__init__(True, None)
        self.node = node
        self.attribute_name = attribute_name
        self.position = position


class AttributeAssignNode(AstNode):
    def __init__(self, node, attribute_name, value_node, position) -> None:
        super().__init__(True, None)
        self.node = node
        self.attribute_name = attribute_name
        self.value_node = value_node
        self.position = position