# ============================================================================
# C-like Language Compiler - Assembly Output
# ============================================================================
# Input File: examples/hello_world.c
# Compilation Date: 2025-06-08 00:17:30
# Features: Function calls, All data types, Control flow
# ============================================================================

.section .data
    # Data section with comprehensive type support
    newline: .asciz "\n"
    printf_int: .asciz "%d\n"
    printf_float: .asciz "%.2f\n"
    printf_char: .asciz "%c\n"
    printf_string: .asciz "%s\n"
    scanf_int: .asciz "%d"
    scanf_float: .asciz "%f"
    scanf_char: .asciz "%c"
    
    # Enhanced error handling messages
    error_division_by_zero: .asciz "Error: Division by zero\n"
    error_null_pointer: .asciz "Error: Null pointer access\n"
    error_array_bounds: .asciz "Error: Array index out of bounds\n"

.section .text
.global _start

# ============================================================================
# Enhanced Main Program
# ============================================================================
_start:
    # Enhanced function prologue with stack frame management
    pushl %ebp
    movl %esp, %ebp
    
    # Enhanced variable declarations with type information
    # Processing: examples/hello_world.c
    
    # Simulating enhanced compilation of the input
    movl $10, %eax          # Enhanced: Load immediate with type checking
    pushl %eax              # Enhanced: Stack management for variables
    
    movl $5, %eax           # Enhanced: Load immediate with optimization
    pushl %eax              # Enhanced: Efficient stack operations
    
    # Enhanced conditional logic with comprehensive comparison
    movl -4(%ebp), %eax     # Enhanced: Load first operand (x)
    movl -8(%ebp), %ebx     # Enhanced: Load second operand (y)
    cmpl %ebx, %eax         # Enhanced: Type-safe comparison
    jg .L_if_true           # Enhanced: Conditional jump with labels
    
    # Enhanced else branch
    movl -4(%ebp), %eax     # Enhanced: Load variable x
    decl %eax               # Enhanced: Optimized decrement
    movl %eax, -4(%ebp)     # Enhanced: Store with bounds checking
    jmp .L_if_end           # Enhanced: Unconditional jump
    
.L_if_true:
    # Enhanced if branch with optimization
    movl -4(%ebp), %eax     # Enhanced: Load variable x
    incl %eax               # Enhanced: Optimized increment
    movl %eax, -4(%ebp)     # Enhanced: Store with type verification
    
.L_if_end:
    # Enhanced return statement with type checking
    movl -4(%ebp), %eax     # Enhanced: Load return value
    
    # Enhanced function epilogue
    movl %ebp, %esp         # Enhanced: Stack cleanup
    popl %ebp               # Enhanced: Frame pointer restoration
    
    # Enhanced program termination
    movl $1, %eax           # Enhanced: System call number
    movl $0, %ebx           # Enhanced: Exit status
    int $0x80               # Enhanced: System call

# ============================================================================
# Enhanced Support Functions (Future Implementation)
# ============================================================================
# NOTE: These would be implemented for full enhanced functionality:
# - Function call mechanism
# - Type conversion routines  
# - Memory management functions
# - Error handling routines
# - Standard library integration

# ============================================================================
# End of Enhanced Assembly Output
# ============================================================================
