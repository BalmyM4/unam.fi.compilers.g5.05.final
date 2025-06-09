# Generated Assembly Code
.section .data
newline: .asciz "\n"
printf_int: .asciz "%d\n"
scanf_int: .asciz "%d"

.section .text
.global _start

    movl $85, %eax
    # Assignment to score
    movl $10, %eax
    # Assignment to bonus
    # Load variable score
    movl -18(%ebp), %eax
    pushl %eax
    movl $90, %eax
    movl %eax, %ebx
    popl %eax
    cmpl %ebx, %eax
    setge %al
    movzbl %al, %eax
    # If statement
    cmpl $0, %eax
    je L0
    # Load variable score
    movl -18(%ebp), %eax
    pushl %eax
    # Load variable bonus
    movl -38(%ebp), %eax
    movl %eax, %ebx
    popl %eax
    addl %ebx, %eax
    # Assignment to final_score
    # Load variable final_score
    movl -54(%ebp), %eax
    pushl %eax
    movl $100, %eax
    movl %eax, %ebx
    popl %eax
    cmpl %ebx, %eax
    setg %al
    movzbl %al, %eax
    # If statement
    cmpl $0, %eax
    je L2
    movl $100, %eax
    # Assignment to final_score
    jmp L3
L2:
L3:
    jmp L1
L0:
    # Load variable score
    movl -18(%ebp), %eax
    pushl %eax
    movl $70, %eax
    movl %eax, %ebx
    popl %eax
    cmpl %ebx, %eax
    setge %al
    movzbl %al, %eax
    # If statement
    cmpl $0, %eax
    je L4
    # Load variable score
    movl -18(%ebp), %eax
    pushl %eax
    # Load variable bonus
    movl -38(%ebp), %eax
    pushl %eax
    movl $2, %eax
    movl %eax, %ebx
    popl %eax
    cdq
    idivl %ebx
    movl %eax, %ebx
    popl %eax
    addl %ebx, %eax
    # Assignment to final_score
    jmp L5
L4:
    # Load variable score
    movl -18(%ebp), %eax
    # Assignment to final_score
L5:
L1:
    # Load variable final_score
    movl -54(%ebp), %eax
    # Return statement
    movl %ebp, %esp
    popl %ebp
    ret

# Exit program
movl $1, %eax
movl $0, %ebx
int $0x80