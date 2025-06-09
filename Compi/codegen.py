from parser import *

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.label_count = 0
        self.var_offset = {}
        self.current_offset = 0
    
    def generate(self, ast):
        self.visit(ast)
        return '\n'.join(self.code)
    
    def emit(self, instruction):
        self.code.append(instruction)
    
    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"
    
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        pass
    
    def visit_Program(self, node):
        self.emit(".section .text")
        self.emit(".globl _start")
        self.emit("_start:")
        for stmt in node.statements:
            self.visit(stmt)
        self.emit("movl $1, %eax")
        self.emit("movl $0, %ebx")
        self.emit("int $0x80")
    
    def visit_FunctionDef(self, node):
        self.emit(f"{node.name}:")
        self.emit("pushl %ebp")
        self.emit("movl %esp, %ebp")
        self.visit(node.body)
        self.emit("popl %ebp")
        self.emit("ret")
    
    def visit_VarDecl(self, node):
        self.current_offset -= 4
        self.var_offset[node.name] = self.current_offset
        self.emit(f"subl $4, %esp")
        if node.init_value:
            self.visit(node.init_value)
            self.emit(f"movl %eax, {self.current_offset}(%ebp)")
    
    def visit_Assignment(self, node):
        self.visit(node.value)
        offset = self.var_offset[node.name]
        self.emit(f"movl %eax, {offset}(%ebp)")
    
    def visit_IfStmt(self, node):
        else_label = self.new_label()
        end_label = self.new_label()
        
        self.visit(node.condition)
        self.emit("cmpl $0, %eax")
        self.emit(f"je {else_label}")
        
        self.visit(node.then_stmt)
        self.emit(f"jmp {end_label}")
        
        self.emit(f"{else_label}:")
        if node.else_stmt:
            self.visit(node.else_stmt)
        
        self.emit(f"{end_label}:")
    
    def visit_ForStmt(self, node):
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.visit(node.init)
        
        self.emit(f"{start_label}:")
        self.visit(node.condition)
        self.emit("cmpl $0, %eax")
        self.emit(f"je {end_label}")
        
        self.visit(node.body)
        self.visit(node.update)
        self.emit(f"jmp {start_label}")
        
        self.emit(f"{end_label}:")
    
    def visit_ReturnStmt(self, node):
        if node.value:
            self.visit(node.value)
        self.emit("popl %ebp")
        self.emit("ret")
    
    def visit_Block(self, node):
        for stmt in node.statements:
            self.visit(stmt)
    
    def visit_BinaryOp(self, node):
        self.visit(node.left)
        self.emit("pushl %eax")
        self.visit(node.right)
        self.emit("popl %ebx")
        
        if node.op == '+':
            self.emit("addl %ebx, %eax")
        elif node.op == '-':
            self.emit("subl %eax, %ebx")
            self.emit("movl %ebx, %eax")
        elif node.op == '*':
            self.emit("imull %ebx, %eax")
        elif node.op == '/':
            self.emit("movl %ebx, %eax")
            self.emit("cdq")
            self.emit("idivl %ebx")
        elif node.op == '==':
            self.emit("cmpl %eax, %ebx")
            self.emit("sete %al")
            self.emit("movzbl %al, %eax")
        elif node.op == '!=':
            self.emit("cmpl %eax, %ebx")
            self.emit("setne %al")
            self.emit("movzbl %al, %eax")
        elif node.op == '<':
            self.emit("cmpl %eax, %ebx")
            self.emit("setl %al")
            self.emit("movzbl %al, %eax")
        elif node.op == '>':
            self.emit("cmpl %eax, %ebx")
            self.emit("setg %al")
            self.emit("movzbl %al, %eax")
    
    def visit_Identifier(self, node):
        offset = self.var_offset[node.name]
        self.emit(f"movl {offset}(%ebp), %eax")
    
    def visit_Number(self, node):
        self.emit(f"movl ${node.value}, %eax")
