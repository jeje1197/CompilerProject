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

mod_int = """
"""