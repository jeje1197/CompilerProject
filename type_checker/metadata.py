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
    def __init__(self, name) -> None:
        self.name = name
        self.fields = {}

    def add_field(self, field_name, data_type):
        if field_name in self.fields:
            return False
        self.fields[field_name] = data_type
        return True
    
    def get_field(self, field_name):
        return self.fields.get(field_name, None)

    
