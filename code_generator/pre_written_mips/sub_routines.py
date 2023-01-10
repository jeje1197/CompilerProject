add_mips = """
add_int:
	# Store ret addr on top of args on stack
	# Stack ( a, b, ra)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4

	# Get two values from stack in $a0, $t0
	# Stack (a, b, ra)top
	#        ^  ^
	#       12  8  4  0
	lw  $a0, 12($sp)
	lw  $t0, 8($sp)
	
	# Add two values and store result in $a0
	add $a0, $a0, $t0
	
	# Pop ret addr into reg $t0
	lw $t0, 4($sp)
	
	# Clear stack
	# Stack ()
	addiu $sp, $sp, 12
	
	# Place result on top of stack
	# Stack (res)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4
	
	# Jump to ret addr
	jr $t0
"""

sub_mips = """
sub_int:
	# Store ret addr on top of args on stack
	# Stack ( a, b, ra)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4

	# Get two values from stack in $a0, $t0
	# Stack (a, b, ra)top
	#        ^  ^
	#       12  8  4  0
	lw  $a0, 12($sp)
	lw  $t0, 8($sp)
	
	# Add two values and store result in $a0
	sub $a0, $a0, $t0
	
	# Pop ret addr into reg $t0
	lw $t0, 4($sp)
	
	# Clear stack
	# Stack ()
	addiu $sp, $sp, 12
	
	# Place result on top of stack
	# Stack (res)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4
	
	# Jump to ret addr
	jr $t0
"""

mul_mips = """
mul_int:
	# Store ret addr on top of args on stack
	# Stack ( a, b, ra)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4

	# Get two values from stack in $a0, $t0
	# Stack (a, b, ra)top
	#        ^  ^
	#       12  8  4  0
	lw  $a0, 12($sp)
	lw  $t0, 8($sp)
	
	# Mul two values and store result in $a0
	mult $a0, $t0
    mflo $a0
	
	# Pop ret addr into reg $t0
	lw $t0, 4($sp)
	
	# Clear stack
	# Stack ()
	addiu $sp, $sp, 12
	
	# Place result on top of stack
	# Stack (res)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4
	
	# Jump to ret addr
	jr $t0
"""

div_mips = """
div_int:
	# Store ret addr on top of args on stack
	# Stack ( a, b, ra)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4

	# Get two values from stack in $a0, $t0
	# Stack (a, b, ra)top
	#        ^  ^
	#       12  8  4  0
	lw  $a0, 12($sp)
	lw  $t0, 8($sp)
	
	# Div two values and store result in $a0
	div $a0, $a0, $t0
    mflo $a0
	
	# Pop ret addr into reg $t0
	lw $t0, 4($sp)
	
	# Clear stack
	# Stack ()
	addiu $sp, $sp, 12
	
	# Place result on top of stack
	# Stack (res)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4
	
	# Jump to ret addr
	jr $t0
"""

mod_mips = """
mod_int:
	# Store ret addr on top of args on stack
	# Stack ( a, b, ra)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4

	# Get two values from stack in $a0, $t0
	# Stack (a, b, ra)top
	#        ^  ^
	#       12  8  4  0
	lw  $a0, 12($sp)
	lw  $t0, 8($sp)
	
	# Mod two values and store result in $a0
	div $a0, $a0, $t0
    mfhi $a0
	
	# Pop ret addr into reg $t0
	lw $t0, 4($sp)
	
	# Clear stack
	# Stack ()
	addiu $sp, $sp, 12
	
	# Place result on top of stack
	# Stack (res)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4
	
	# Jump to ret addr
	jr $t0
"""

print_int_mips = """
print_int:
	# Store ret addr on top of args on stack
	# Stack (a, ra)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4

	# Print integer from top of stack
	li $v0, 1
    lw $a0, 8($sp)
    syscall

	# Pop ret addr into reg $t0
	lw $t0, 4($sp)
	addiu $sp, $sp, 8

	# Jump to ret addr
	jr $t0
"""
print_char_mips = """
print_char:
	# Print character from top of stack
	# Store ret addr on top of args on stack
	# Stack (a, ra)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4

	# Print char from top of stack
	li $v0, 11
    lw $a0, 8($sp)
    syscall

	# Pop ret addr into reg $t0
	lw $t0, 4($sp)
	addiu $sp, $sp, 8

	# Jump to ret addr
	jr $t0
"""

print_string_mips = """
print_string:
	# Print string from address on top of stack
	# Store ret addr on top of args on stack
	# Stack (a, ra)
	sw $a0, 0($sp)
	addiu $sp, $sp, -4

	# Print string from address on top of stack
	li $v0, 4
    lw $a0, 8($sp)
    syscall

	# Pop ret addr into reg $t0
	lw $t0, 4($sp)
	addiu $sp, $sp, 8

	# Jump to ret addr
	jr $t0
"""

prewritten_mips = "".join([
	add_mips,
	sub_mips,
	mul_mips,
	div_mips,
	mod_mips,
	print_int_mips,
	print_char_mips,
	print_string_mips
])