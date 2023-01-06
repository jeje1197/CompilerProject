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

PLUS = [
    [],
]

operation = {
    '+',
    '-',
    '*',
    '/',
    '%',
    '<',
    '>',
    '<=',
    '>=',
    '==',
    '!=',
    '&&',
    '||'
}