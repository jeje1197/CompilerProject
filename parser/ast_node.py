class AstNode:
    def __init__(self, is_expr=None, data_type=None):
        self.is_expr = is_expr
        self.data_type = data_type

    def __repr__(self) -> str:
        return f'(AstNode {type(self).__name__}: is_expr: {self.is_expr} data_type: {self.data_type}'


class UnaryOpNode(AstNode):
    def __init__(self, op, node, position) -> None:
        super(True, None)
        self.op = op
        self.node = node
        self.position = position


class BinOpNode(AstNode):
    def __init__(self, left_node, op, right_node, position) -> None:
        super(True, None)
        self.left_node = left_node
        self.op = op
        self.right_node = right_node
        self.position = left_node.position


class IntNode(AstNode):
    def __init__(self, value, position) -> None:
        super(True, 'int')
        self.value = value
        self.position = position


class FloatNode(AstNode):
    def __init__(self, value, position) -> None:
        super(True, 'float')
        self.value = value
        self.position = position


class CharNode(AstNode):
    def __init__(self, value, position) -> None:
        super(True, 'char')
        self.value = value
        self.position = position


class StringNode(AstNode):
    def __init__(self, value, position) -> None:
        super(True, 'char*')
        self.value = value
        self.position = position


class VarDeclarationNode(AstNode):
    def __init__(self, type, var_name, node, position) -> None:
        super(True, type)
        self.var_name = var_name
        self.node = node
        self.position = position


class VarAssignNode(AstNode):
    def __init__(self, var_name, node, position) -> None:
        super(True, None)
        self.var_name = var_name
        self.node = node
        self.position = position


class VarAccessNode(AstNode):
    def __init__(self, var_name, position) -> None:
        super(True, 'char*')
        self.var_name = var_name
        self.position = position


class IfNode(AstNode):
    def __init__(self, case_conditions, case_statements, else_statements, position) -> None:
        super(True, None)
        self.case_conditions = case_conditions
        self.case_statements = case_statements
        self.else_statements = else_statements
        self.position = position


class WhileNode(AstNode):
    def __init__(self, cond_node, statements, position) -> None:
        super(True, None)
        self.cond_node = cond_node
        self.statements = statements
        self.position = position


class FunctionNode(AstNode):
    def __init__(self, name, args_w_types, return_type, statements, position) -> None:
        super(True, return_type)
        self.name = name
        self.args_w_types = args_w_types
        self.return_type = return_type
        self.statements = statements
        self.position = position


class StructNode(AstNode):
    def __init__(self, name, statements, position) -> None:
        super(True, None)
        self.name = name
        self.statements = statements
        self.position = position