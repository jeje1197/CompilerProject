from type_checker import metadata

print_int_fn = metadata.FunctionDefinition(
    'printint', 
    [('integer', 'int')], 
    'void'
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