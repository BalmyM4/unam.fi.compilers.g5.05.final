# Generated Assembly Code
.section .data
newline: .asciz "\n"
printf_int: .asciz "%d\n"
scanf_int: .asciz "%d"

.section .text
.global _start

    movl $15, %eax
    # Assignment to a
    movl $10, %eax
    # Assignment to b
    movl $20, %eax
    # Assignment to c
    # Load variable a
    movl -8(%ebp), %eax
    pushl %eax
    # Load variable b
    movl -4(%ebp), %eax
    movl %eax, %ebx
    popl %eax
    cmpl %ebx, %eax
    setg %al
    movzbl %al, %eax
    # If statement
    cmpl $0, %eax
    je L0
    # Load variable a
    movl -8(%ebp), %eax
    pushl %eax
    # Load variable c
    movl -23(%ebp), %eax
    movl %eax, %ebx
    popl %eax
    cmpl %ebx, %eax
    setg %al
    movzbl %al, %eax
    # If statement
    cmpl $0, %eax
    je L2
    # Load variable a
    movl -8(%ebp), %eax
    pushl %eax
    movl $2, %eax
    movl %eax, %ebx
    popl %eax
    imull %ebx, %eax
    # Assignment to a
    jmp L3
L2:
    # Load variable c
    movl -23(%ebp), %eax
    # Assignment to a
L3:
    jmp L1
L0:
    # Load variable b
    movl -4(%ebp), %eax
    # Assignment to a
L1:
    # Load variable a
    movl -8(%ebp), %eax
    # Return statement
    movl %ebp, %esp
    popl %ebp
    ret

# Exit program
movl $1, %eax
movl $0, %ebx
int $0x80