#!/usr/bin/env python3

"""
AST Node definitions for the C-like language compiler
Student Implementation
"""

class ASTNode:
    """Base class for all AST nodes"""
    def __init__(self):
        self.line_number = None
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

# Program structure
class Program(ASTNode):
    def __init__(self, declarations):
        super().__init__()
        self.declarations = declarations

class TranslationUnit(ASTNode):
    def __init__(self, external_declarations):
        super().__init__()
        self.external_declarations = external_declarations

# Declarations
class Declaration(ASTNode):
    pass

class FunctionDecl(Declaration):
    def __init__(self, return_type, name, parameters, body=None):
        super().__init__()
        self.return_type = return_type
        self.name = name
        self.parameters = parameters or []
        self.body = body

class VariableDecl(Declaration):
    def __init__(self, var_type, declarators):
        super().__init__()
        self.var_type = var_type
        self.declarators = declarators

class Declarator(ASTNode):
    def __init__(self, name, initializer=None):
        super().__init__()
        self.name = name
        self.initializer = initializer

class Parameter(ASTNode):
    def __init__(self, param_type, name):
        super().__init__()
        self.param_type = param_type
        self.name = name

# Type system
class Type(ASTNode):
    def __init__(self, base_type, modifiers=None):
        super().__init__()
        self.base_type = base_type
        self.modifiers = modifiers or []

class BasicType(Type):
    def __init__(self, type_name):
        super().__init__(type_name)
        self.type_name = type_name

class PointerType(Type):
    def __init__(self, base_type):
        super().__init__(base_type)
        self.base_type = base_type

class ArrayType(Type):
    def __init__(self, base_type, size=None):
        super().__init__(base_type)
        self.base_type = base_type
        self.size = size

# Statements
class Statement(ASTNode):
    pass

class CompoundStmt(Statement):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

class ExpressionStmt(Statement):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression

class IfStmt(Statement):
    def __init__(self, condition, then_stmt, else_stmt=None):
        super().__init__()
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

class WhileStmt(Statement):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

class ForStmt(Statement):
    def __init__(self, init, condition, update, body):
        super().__init__()
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class DoWhileStmt(Statement):
    def __init__(self, body, condition):
        super().__init__()
        self.body = body
        self.condition = condition

class ReturnStmt(Statement):
    def __init__(self, value=None):
        super().__init__()
        self.value = value

class BreakStmt(Statement):
    pass

class ContinueStmt(Statement):
    pass

class SwitchStmt(Statement):
    def __init__(self, expression, body):
        super().__init__()
        self.expression = expression
        self.body = body

class CaseStmt(Statement):
    def __init__(self, value, statements):
        super().__init__()
        self.value = value
        self.statements = statements

class DefaultStmt(Statement):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

# Expressions
class Expression(ASTNode):
    pass

class BinaryOp(Expression):
    def __init__(self, left, operator, right):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right

class UnaryOp(Expression):
    def __init__(self, operator, operand, prefix=True):
        super().__init__()
        self.operator = operator
        self.operand = operand
        self.prefix = prefix  # True for prefix, False for postfix

class TernaryOp(Expression):
    def __init__(self, condition, true_expr, false_expr):
        super().__init__()
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

class AssignmentExpr(Expression):
    def __init__(self, left, operator, right):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right

class FunctionCall(Expression):
    def __init__(self, function, arguments):
        super().__init__()
        self.function = function
        self.arguments = arguments or []

class ArrayAccess(Expression):
    def __init__(self, array, index):
        super().__init__()
        self.array = array
        self.index = index

class MemberAccess(Expression):
    def __init__(self, object_expr, member, is_pointer=False):
        super().__init__()
        self.object_expr = object_expr
        self.member = member
        self.is_pointer = is_pointer  # True for ->, False for .

class SizeofExpr(Expression):
    def __init__(self, operand):
        super().__init__()
        self.operand = operand

class CastExpr(Expression):
    def __init__(self, target_type, expression):
        super().__init__()
        self.target_type = target_type
        self.expression = expression

# Literals
class Literal(Expression):
    def __init__(self, value):
        super().__init__()
        self.value = value

class IntegerLiteral(Literal):
    def __init__(self, value):
        super().__init__(value)

class FloatLiteral(Literal):
    def __init__(self, value):
        super().__init__(value)

class CharLiteral(Literal):
    def __init__(self, value):
        super().__init__(value)

class StringLiteral(Literal):
    def __init__(self, value):
        super().__init__(value)

class BoolLiteral(Literal):
    def __init__(self, value):
        super().__init__(value)

# Identifiers
class Identifier(Expression):
    def __init__(self, name):
        super().__init__()
        self.name = name

# Initializers
class Initializer(ASTNode):
    pass

class ExpressionInitializer(Initializer):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression

class InitializerList(Initializer):
    def __init__(self, initializers):
        super().__init__()
        self.initializers = initializers

# Helper functions for AST construction
def make_binary_op(left, op, right):
    """Helper function to create binary operations"""
    return BinaryOp(left, op, right)

def make_unary_op(op, operand, prefix=True):
    """Helper function to create unary operations"""
    return UnaryOp(op, operand, prefix)

def make_function_call(func_name, args):
    """Helper function to create function calls"""
    if isinstance(func_name, str):
        func_name = Identifier(func_name)
    return FunctionCall(func_name, args)

def make_assignment(left, op, right):
    """Helper function to create assignments"""
    return AssignmentExpr(left, op, right)
