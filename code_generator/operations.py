# Stack machine operations translated to mips assembly

def gen_push_int(asm_text:list[str], int_value:int):
    asm_text.extend([
        '# Push int to stack',
        f'li $a0, {int_value}',
        'sw $a0, 0($sp)',
        'addiu $sp, $sp, -4',
        ''
    ])

def gen_add_int(asm_text:list[str]):
    asm_text.extend([
        '# Addition on top two from stack  -> result stored on top of stack',
        'la $t0, add_int',
        'jalr $a0, $t0'
        ''
    ])

def gen_sub_int(asm_text:list[str]):
    asm_text.extend([
        '# Subtraction on top two from stack  -> result stored on top of stack',
        'la $t0, sub_int',
        'jalr $a0, $t0'
        ''
    ])

def gen_mul_int(asm_text:list[str]):
    asm_text.extend([
        '# Multiplication on top two from stack -> result stored on top of stack',
        'la $t0, mul_int',
        'jalr $a0, $t0'
        ''
    ])

def gen_div_int(asm_text:list[str]):
    asm_text.extend([
        '# Division on top two from stack -> result stored on top of stack',
        'la $t0, div_int',
        'jalr $a0, $t0'
        ''
    ])

def gen_mod_int(asm_text:list[str]):
    asm_text.extend([
        '# Modulo on top two from stack -> result stored on top of stack',
        'lw $a0, 8($sp)',
        'lw $t0, 4($sp)',
        'addiu $sp, $sp, 8',
        'div $a0, $a0, $t0',
        'mfhi $a0',
        'sw $a0, 0($sp)',
        'addiu $sp, $sp, -4',
        ''
    ])

def gen_lt_int(asm_text:list[str]):
    asm_text.extend([
        '# Perform less than on top two from stack -> result stored on top of stack',
        'lw $a0, 8($sp)',
        'lw $t0, 4($sp)',
        'addiu $sp, $sp, 8',
        'slt $a0, $a0, $t0',
        'sw $a0, 0($sp)',
        'addiu $sp, $sp, -4',
        ''
    ])

def gen_gt_int(asm_text:list[str]):
    asm_text.extend([
        '# Perform greater than on top two from stack -> result stored on top of stack',
        'lw $a0, 8($sp)',
        'lw $t0, 4($sp)',
        'addiu $sp, $sp, 8',
        'slt $a0, $t0, $a0',
        'sw $a0, 0($sp)',
        'addiu $sp, $sp, -4',
        ''
    ])




# Print
def gen_print_int(asm_text:list[str]):
    asm_text.extend([
        '# Print integer from top of stack',
        'li $v0, 1'
        'lw $a0, 4($sp)',
        'addiu $sp, $sp, 4',
        'syscall',
        ''
    ])

def gen_print_char(asm_text:list[str]):
    asm_text.extend([
        '# Print char from top of stack',
        'li $v0, 11'
        'lw $a0, 4($sp)',
        'addiu $sp, $sp, 4',
        'syscall',
        ''
    ])

def gen_print_string(asm_text:list[str]):
    asm_text.extend([
        '# Print string from address on top of stack',
        'li $v0, 4'
        'lw $a0, 4($sp)',
        'addiu $sp, $sp, 4',
        'syscall',
    ])
