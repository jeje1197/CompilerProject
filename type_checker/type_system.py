class TypeSystem:
    """
    A system that manages the valid types in the language and validates
    typecasting
    """
    def __init__(self) -> None:
        self.declared_types = {
            'void': [],
            'int': ['char', 'float'],
            'float': ['int'],
            'char': ['int'],
        }

        self.auto_cast = {
            'void': [],
            'int': ['char', 'float'],
            'float': [],
            'char': ['int']
        }

    def add_type(self, new_type):
        self.declared_types[new_type] == []
        self.auto_cast[new_type] == []

    def get_base_type_from_ptr(self, type):
        """
        Returns a string without any '*' in it
        """
        base_type = ''
        for c in type:
            if c == '*':
                break
            base_type += c
        return base_type

    def is_valid_type(self, type):
        return self.get_base_type_from_ptr(type) in self.declared_types

    def is_pointer_type(self, type):
        return '*' in type

    def create_pointer_type(self, type):
        return type + '*'

    def dereference_pointer_type(self, type):
        return type[:-1]

    def type_matches(self, type, desired_type):
        return type == desired_type or desired_type in self.auto_cast.get(type, ())

    def type_castable(self, type, desired_type):
        if not self.is_valid_type(desired_type):
            return False

        cast_list = self.declared_types.get(type, ())
        if self.type_matches(type, desired_type):
            return True
        elif self.is_pointer_type(type) and desired_type in ('int', 'void*'):
            return True
        elif type == 'void*' and self.is_pointer_type(desired_type):
            return True
        else:
            return desired_type in cast_list

    def get_type_from_unary_op(self, type, op):
        if op == '-':
            if type == 'char':
                return 'int'
            else:
                return type
        elif op == '*':
            if not self.is_pointer_type(type):
                return None
            else:
                return self.dereference_pointer_type(type)
        elif op == '&':
            return self.create_pointer_type(type)

    def get_type_from_bin_op(self, left_type, op, right_type):
        if op == '+':
            return self.add(left_type, right_type)
        elif op == '-':
            return self.sub(left_type, right_type)
        elif op == '*':
            return self.mul(left_type, right_type)
        elif op == '/':
            return self.div(left_type, right_type)
        elif op == '%':
            return self.mod(left_type, right_type)
        elif op in ('<', '>', '<=', '>='):
            return self.lt_gt_lte_gte_comparisons(left_type, right_type)
        elif op in ('==', '!='):
            return self.ee_ne_comparisons(left_type, right_type)
        else:
            return None

    def add(self, left_type, right_type):
        type_tuples = [(left_type, right_type), (right_type, left_type)]
        if ('int', 'int') in type_tuples:
            return 'int'
        elif ('float', 'float') in type_tuples:
            return 'float'
        elif ('int', 'float') in type_tuples:
            return 'float'
        elif ('char', 'char') in type_tuples:
            return 'char'
        elif ('int', 'char') in type_tuples:
            return 'int'
        elif ('int', 'void*') in type_tuples:
            return 'int'
        else: 
            return None
        
    def sub(self, left_type, right_type):
        type_tuples = [(left_type, right_type), (right_type, left_type)]
        if ('int', 'int') in type_tuples:
            return 'int'
        elif ('float', 'float') in type_tuples:
            return 'float'
        elif ('int', 'float') in type_tuples:
            return 'float'
        elif ('char', 'char') in type_tuples:
            return 'char'
        elif ('int', 'char') in type_tuples:
            return 'int'
        elif ('int', 'void*') in type_tuples:
            return 'int'
        else: 
            return None

    def mul(self, left_type, right_type):
        type_tuples = [(left_type, right_type), (right_type, left_type)]
        if ('int', 'int') in type_tuples:
            return 'int'
        elif ('float', 'float') in type_tuples:
            return 'float'
        elif ('int', 'float') in type_tuples:
            return 'float'
        else:
            return None

    def div(self, left_type, right_type):
        type_tuples = [(left_type, right_type), (right_type, left_type)]
        if ('int', 'int') in type_tuples:
            return 'int'
        elif ('float', 'float') in type_tuples:
            return 'float'
        elif ('int', 'float') in type_tuples:
            return 'float'
        else:
            return None

    def mod(self, left_type, right_type):
        type_tuples = [(left_type, right_type), (right_type, left_type)]
        if ('int', 'int') in type_tuples:
            return 'int'
        elif ('float', 'float') in type_tuples:
            return 'int'
        elif ('int', 'float') in type_tuples:
            return 'float'
        else:
            return None

    def lt_gt_lte_gte_comparisons(self, left_type, right_type):
        type_tuples = [(left_type, right_type), (right_type, left_type)]
        if ('int', 'int') in type_tuples:
            return 'int'
        elif ('int', 'float') in type_tuples:
            return 'int'
        elif ('int', 'char') in type_tuples:
            return 'int'
        else:
            return None

    def ee_ne_comparisons(self, left_type, right_type):
        type_tuples = [(left_type, right_type), (right_type, left_type)]
        if left_type == right_type:
            return 'int'
        elif ('int', 'float') in type_tuples:
            return 'int'
        elif ('int', 'char') in type_tuples:
            return 'int'
        else:
            return None
        