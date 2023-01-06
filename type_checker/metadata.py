class Metadata:
    def __init__(self, sum_type, metadata) -> None:
        self.sum_type = sum_type
        self.metadata = metadata

    def get_sum_type(self):
        return self.sum_type

    def get_metadata(self):
        return self.metadata

class FunctionDefinition:
    def __init__(self, name, args_w_types, return_type) -> None:
        self.name = name
        self.args_w_types = args_w_types
        self.return_type = return_type

class StructDefinition:
    def __init__(self, type, fields_w_types) -> None:
        self.type = type
        self.fields_w_types = fields_w_types
    
