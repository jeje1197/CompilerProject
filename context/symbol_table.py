class SymbolTable:
    def __init__(self, parent=None) -> None:
        self.symbols = dict()

    def contains_local(self, key):
        return key in self.symbols

    def contains_anywhere(self, key):
        symbol_table = self

        while symbol_table:
            if symbol_table.contains_local(key):
                return True
            symbol_table = symbol_table.parent
        return False

    def set_local(self, key, value):
        self.symbols[key] = value

    def set_in_lowest_scope(self, key, value):
        symbol_table = self

        while symbol_table:
            if symbol_table.contains_local(key):
                symbol_table.set_local(key, value)
                return
            symbol_table = symbol_table.parent
        self.set_local(key, value)

    def get_local(self, key):
        return self.symbols[key]

    def get(self, key):
        symbol_table = self

        while symbol_table:
            if symbol_table.contains_local(key):
                return symbol_table.get_local(key)
            symbol_table = symbol_table.parent

    def generate_sub_context(self):
        return SymbolTable(self)