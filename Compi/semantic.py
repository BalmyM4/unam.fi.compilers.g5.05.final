from parser import *

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None
    
    def define(self, name, symbol_type):
        self.symbols[name] = symbol_type
    
    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
    
    def analyze(self, ast):
        self.visit(ast)
        return self.errors
    
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        for child in getattr(node, '__dict__', {}).values():
            if isinstance(child, list):
                for item in child:
                    if isinstance(item, ASTNode):
                        self.visit(item)
            elif isinstance(child, ASTNode):
                self.visit(child)
    
    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)
    
    def visit_FunctionDef(self, node):
        self.symbol_table.define(node.name, node.return_type)
        old_table = self.symbol_table
        self.symbol_table = SymbolTable()
        self.symbol_table.parent = old_table
        
        for param in node.params:
            self.visit(param)
        self.visit(node.body)
        
        self.symbol_table = old_table
    
    def visit_VarDecl(self, node):
        if self.symbol_table.lookup(node.name):
            self.errors.append(f"Variable '{node.name}' already declared")
        self.symbol_table.define(node.name, node.var_type)
        if node.init_value:
            self.visit(node.init_value)
    
    def visit_Assignment(self, node):
        if not self.symbol_table.lookup(node.name):
            self.errors.append(f"Variable '{node.name}' not declared")
        self.visit(node.value)
    
    def visit_IfStmt(self, node):
        self.visit(node.condition)
        self.visit(node.then_stmt)
        if node.else_stmt:
            self.visit(node.else_stmt)
    
    def visit_ForStmt(self, node):
        self.visit(node.init)
        self.visit(node.condition)
        self.visit(node.update)
        self.visit(node.body)
    
    def visit_ReturnStmt(self, node):
        if node.value:
            self.visit(node.value)
    
    def visit_Block(self, node):
        old_table = self.symbol_table
        self.symbol_table = SymbolTable()
        self.symbol_table.parent = old_table
        
        for stmt in node.statements:
            self.visit(stmt)
        
        self.symbol_table = old_table
    
    def visit_BinaryOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
    
    def visit_Identifier(self, node):
        if not self.symbol_table.lookup(node.name):
            self.errors.append(f"Variable '{node.name}' not declared")
    
    def visit_Number(self, node):
        pass
