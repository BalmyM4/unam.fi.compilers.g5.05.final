# Generated Assembly Code
.section .data
newline: .asciz "\n"
printf_int: .asciz "%d\n"
scanf_int: .asciz "%d"

.section .text
.global _start

    movl $8, %eax
    # Assignment to x
    movl $3, %eax
    # Assignment to y
    # Load variable x
    movl -49(%ebp), %eax
    pushl %eax
    movl $5, %eax
    movl %eax, %ebx
    popl %eax
    cmpl %ebx, %eax
    setg %al
    movzbl %al, %eax
    pushl %eax
    # Load variable y
    movl -35(%ebp), %eax
    pushl %eax
    movl $10, %eax
    movl %eax, %ebx
    popl %eax
    cmpl %ebx, %eax
    setl %al
    movzbl %al, %eax
    movl %eax, %ebx
    popl %eax
    cmpl $0, %eax
    je L2
    cmpl $0, %ebx
    je L2
    movl $1, %eax
    jmp L2_end
L2:
    movl $0, %eax
L2_end:
    # If statement
    cmpl $0, %eax
    je L0
    # Load variable x
    movl -49(%ebp), %eax
    pushl %eax
    # Load variable y
    movl -35(%ebp), %eax
    pushl %eax
    movl $2, %eax
    movl %eax, %ebx
    popl %eax
    imull %ebx, %eax
    movl %eax, %ebx
    popl %eax
    addl %ebx, %eax
    # Assignment to result
    # Load variable result
    movl -34(%ebp), %eax
    pushl %eax
    movl $10, %eax
    movl %eax, %ebx
    popl %eax
    cmpl %ebx, %eax
    setg %al
    movzbl %al, %eax
    # If statement
    cmpl $0, %eax
    je L3
    # Load variable result
    movl -34(%ebp), %eax
    pushl %eax
    movl $5, %eax
    movl %eax, %ebx
    popl %eax
    subl %ebx, %eax
    # Assignment to result
    jmp L4
L3:
L4:
    jmp L1
L0:
    movl $0, %eax
    # Assignment to result
L1:
    # Load variable result
    movl -34(%ebp), %eax
    # Return statement
    movl %ebp, %esp
    popl %ebp
    ret

# Exit program
movl $1, %eax
movl $0, %ebx
int $0x80