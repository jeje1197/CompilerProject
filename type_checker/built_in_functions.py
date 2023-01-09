from type_checker import metadata

print_int_fn = metadata.FunctionDefinition(
    'printint', 
    [('integer', 'int')], 
    'void',
)

print_char_fn = metadata.FunctionDefinition(
    'printchar', 
    [('character', 'int')],
    'void'
)

print_string_fn = metadata.FunctionDefinition(
    'printstr', 
    [('character', 'int')],
    'void'
)

list_of_fn = [
    ('printi', print_int_fn),
    ('printc', print_char_fn),
    ('printstr', print_string_fn)
]

def add_metadata_to_symbol_table(symbol_table):
    for fn in list_of_fn:
        symbol_table.set_local(fn[0], metadata.Metadata(fn[1].return_type, fn[1]))

def add_function_def_to_symbol_table(symbol_table):
    for fn in list_of_fn:
        symbol_table.set_local(fn[0], fn[1])