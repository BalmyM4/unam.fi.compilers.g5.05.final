# Generated Assembly Code
.section .data
newline: .asciz "\n"
printf_int: .asciz "%d\n"
scanf_int: .asciz "%d"

.section .text
.global _start

    movl $10, %eax
    # Assignment to x
    movl $5, %eax
    # Assignment to y
    # Load variable x
    movl -31(%ebp), %eax
    pushl %eax
    # Load variable y
    movl -9(%ebp), %eax
    movl %eax, %ebx
    popl %eax
    cmpl %ebx, %eax
    setg %al
    movzbl %al, %eax
    # If statement
    cmpl $0, %eax
    je L0
    # Load variable x
    movl -31(%ebp), %eax
    pushl %eax
    movl $1, %eax
    movl %eax, %ebx
    popl %eax
    addl %ebx, %eax
    # Assignment to x
    jmp L1
L0:
    # Load variable x
    movl -31(%ebp), %eax
    pushl %eax
    movl $1, %eax
    movl %eax, %ebx
    popl %eax
    subl %ebx, %eax
    # Assignment to x
L1:
    # Load variable x
    movl -31(%ebp), %eax
    # Return statement
    movl %ebp, %esp
    popl %ebp
    ret

# Exit program
movl $1, %eax
movl $0, %ebx
int $0x80