from type_checker import metadata

print_int_fn = metadata.FunctionDefinition(
    'print_i', 
    [('integer', 'int')], 
    'void',
)

print_char_fn = metadata.FunctionDefinition(
    'print_c', 
    [('character', 'int')],
    'void'
)

print_string_fn = metadata.FunctionDefinition(
    'print_s', 
    [('character', 'int')],
    'void'
)

list_of_fn = [
    ('print_i', print_int_fn),
    ('print_c', print_char_fn),
    ('print_s', print_string_fn)
]

def add_metadata_to_symbol_table(symbol_table):
    for fn in list_of_fn:
        symbol_table.set_local(fn[0], metadata.Metadata(fn[1].return_type, fn[1]))

def add_function_def_to_symbol_table(symbol_table):
    for fn in list_of_fn:
        symbol_table.set_local(fn[0], fn[1])