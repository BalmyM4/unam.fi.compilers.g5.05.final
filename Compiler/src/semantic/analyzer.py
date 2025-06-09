#!/usr/bin/env python3

"""
Semantic Analyzer for C-like Language
Performs type checking, scope validation, and semantic analysis
"""

try:
    from ..parser.ast_nodes import *
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'parser'))
    from ast_nodes import *

class Symbol:
    """Represents a symbol in the symbol table"""
    def __init__(self, name, symbol_type, data_type, value=None, parameters=None):
        self.name = name
        self.symbol_type = symbol_type  # 'variable', 'function', 'parameter'
        self.data_type = data_type
        self.value = value
        self.parameters = parameters or []  # For functions
        self.is_defined = False
        self.line_number = None

class SymbolTable:
    """Symbol table with scope management"""
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        self.children = []
        if parent:
            parent.children.append(self)
    
    def define(self, name, symbol_type, data_type, value=None, parameters=None):
        """Define a symbol in current scope"""
        if name in self.symbols:
            return False  # Already defined in current scope
        
        symbol = Symbol(name, symbol_type, data_type, value, parameters)
        self.symbols[name] = symbol
        return True
    
    def lookup(self, name):
        """Look up a symbol in current scope and parent scopes"""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup(name)
        return None
    
    def lookup_current_scope(self, name):
        """Look up a symbol only in current scope"""
        return self.symbols.get(name)

class TypeChecker:
    """Type checking and conversion utilities"""
    
    # Type hierarchy for implicit conversions
    TYPE_HIERARCHY = {
        'char': 1, 'signed char': 1, 'unsigned char': 1,
        'short': 2, 'signed short': 2, 'unsigned short': 2,
        'int': 3, 'signed int': 3, 'unsigned int': 3,
        'long': 4, 'signed long': 4, 'unsigned long': 4,
        'float': 5, 'double': 6, 'long double': 7
    }
    
    INTEGER_TYPES = {'char', 'signed char', 'unsigned char', 'short', 'signed short', 
                     'unsigned short', 'int', 'signed int', 'unsigned int', 
                     'long', 'signed long', 'unsigned long'}
    
    FLOATING_TYPES = {'float', 'double', 'long double'}
    
    @classmethod
    def normalize_type(cls, type_str):
        """Normalize type string for comparison"""
        if isinstance(type_str, BasicType):
            type_str = type_str.type_name
        
        # Handle default signed types
        if type_str == 'char':
            return 'char'
        elif type_str == 'short':
            return 'signed short'
        elif type_str == 'int':
            return 'signed int'
        elif type_str == 'long':
            return 'signed long'
        
        return type_str
    
    @classmethod
    def can_convert(cls, from_type, to_type):
        """Check if type conversion is possible"""
        from_type = cls.normalize_type(from_type)
        to_type = cls.normalize_type(to_type)
        
        if from_type == to_type:
            return True
        
        # Void pointer conversions
        if from_type == 'void*' or to_type == 'void*':
            return True
        
        # Numeric conversions
        from_rank = cls.TYPE_HIERARCHY.get(from_type, 0)
        to_rank = cls.TYPE_HIERARCHY.get(to_type, 0)
        
        return from_rank > 0 and to_rank > 0
    
    @classmethod
    def promote_types(cls, type1, type2):
        """Get the promoted type for binary operations"""
        type1 = cls.normalize_type(type1)
        type2 = cls.normalize_type(type2)
        
        rank1 = cls.TYPE_HIERARCHY.get(type1, 0)
        rank2 = cls.TYPE_HIERARCHY.get(type2, 0)
        
        if rank1 >= rank2:
            return type1
        else:
            return type2
    
    @classmethod
    def is_integer_type(cls, type_str):
        """Check if type is an integer type"""
        return cls.normalize_type(type_str) in cls.INTEGER_TYPES
    
    @classmethod
    def is_floating_type(cls, type_str):
        """Check if type is a floating point type"""
        return cls.normalize_type(type_str) in cls.FLOATING_TYPES
    
    @classmethod
    def is_numeric_type(cls, type_str):
        """Check if type is numeric (integer or floating)"""
        return cls.is_integer_type(type_str) or cls.is_floating_type(type_str)

class SemanticAnalyzer:
    """Semantic analyzer with full type checking"""
    
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.errors = []
        self.warnings = []
        self.current_function = None
        self.loop_depth = 0
        
        # Add built-in functions
        self._add_builtin_functions()
    
    def _add_builtin_functions(self):
        """Add built-in functions to global scope"""
        builtins = [
            ('printf', 'int', [Parameter(BasicType('char'), '*format')]),
            ('scanf', 'int', [Parameter(BasicType('char'), '*format')]),
            ('malloc', 'void*', [Parameter(BasicType('unsigned int'), 'size')]),
            ('free', 'void', [Parameter(BasicType('void'), '*ptr')]),
            ('strlen', 'unsigned int', [Parameter(BasicType('char'), '*str')]),
            ('strcpy', 'char*', [Parameter(BasicType('char'), '*dest'), Parameter(BasicType('char'), '*src')]),
        ]
        
        for name, return_type, params in builtins:
            self.global_scope.define(name, 'function', return_type, parameters=params)
    
    def error(self, message, node=None):
        """Add an error message"""
        line_info = f" at line {node.line_number}" if node and hasattr(node, 'line_number') else ""
        self.errors.append(f"Error: {message}{line_info}")
    
    def warning(self, message, node=None):
        """Add a warning message"""
        line_info = f" at line {node.line_number}" if node and hasattr(node, 'line_number') else ""
        self.warnings.append(f"Warning: {message}{line_info}")
    
    def enter_scope(self):
        """Enter a new scope"""
        self.current_scope = SymbolTable(self.current_scope)
    
    def exit_scope(self):
        """Exit current scope"""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
    
    def analyze(self, ast):
        """Perform semantic analysis on the AST"""
        self.errors = []
        self.warnings = []
        self.visit(ast)
        return len(self.errors) == 0
    
    def visit(self, node):
        """Visit an AST node"""
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Generic visitor for unknown node types"""
        pass
    
    def visit_Program(self, node):
        """Visit program node"""
        for decl in node.declarations:
            self.visit(decl)
    
    def visit_FunctionDecl(self, node):
        """Visit function declaration/definition"""
        # Check if function already declared
        existing = self.current_scope.lookup_current_scope(node.name)
        if existing:
            if existing.symbol_type != 'function':
                self.error(f"'{node.name}' redeclared as different kind of symbol", node)
                return
            
            # Check function signature compatibility
            if not self._compatible_function_signatures(existing, node):
                self.error(f"Conflicting types for '{node.name}'", node)
                return
        else:
            # Define the function
            params = []
            for param in node.parameters:
                param_type = self._get_type_string(param.param_type)
                params.append(param)
            
            return_type = self._get_type_string(node.return_type)
            success = self.current_scope.define(node.name, 'function', return_type, parameters=params)
            if not success:
                self.error(f"Function '{node.name}' already defined", node)
                return
        
        # If function has a body, analyze it
        if node.body:
            old_function = self.current_function
            self.current_function = node
            
            # Enter function scope
            self.enter_scope()
            
            # Add parameters to function scope
            for param in node.parameters:
                if param.name:
                    param_type = self._get_type_string(param.param_type)
                    success = self.current_scope.define(param.name, 'parameter', param_type)
                    if not success:
                        self.error(f"Parameter '{param.name}' already defined", node)
            
            # Analyze function body
            self.visit(node.body)
            
            # Exit function scope
            self.exit_scope()
            self.current_function = old_function
    
    def visit_VariableDecl(self, node):
        """Visit variable declaration"""
        var_type = self._get_type_string(node.var_type)
        
        for declarator in node.declarators:
            if isinstance(declarator, Declarator):
                var_name = declarator.name
                
                # Check if variable already defined in current scope
                existing = self.current_scope.lookup_current_scope(var_name)
                if existing:
                    self.error(f"Variable '{var_name}' already defined in current scope", node)
                    continue
                
                # Define the variable
                success = self.current_scope.define(var_name, 'variable', var_type)
                if not success:
                    self.error(f"Failed to define variable '{var_name}'", node)
                
                # Check initializer if present
                if declarator.initializer:
                    init_type = self.visit(declarator.initializer)
                    if init_type and not TypeChecker.can_convert(init_type, var_type):
                        self.error(f"Cannot convert '{init_type}' to '{var_type}' in initialization", node)
    
    def visit_CompoundStmt(self, node):
        """Visit compound statement (block)"""
        self.enter_scope()
        for stmt in node.statements:
            self.visit(stmt)
        self.exit_scope()
    
    def visit_ExpressionStmt(self, node):
        """Visit expression statement"""
        if node.expression:
            self.visit(node.expression)
    
    def visit_IfStmt(self, node):
        """Visit if statement"""
        cond_type = self.visit(node.condition)
        if cond_type and not TypeChecker.is_numeric_type(cond_type):
            self.warning(f"Using non-numeric type '{cond_type}' in condition", node)
        
        self.visit(node.then_stmt)
        if node.else_stmt:
            self.visit(node.else_stmt)
    
    def visit_WhileStmt(self, node):
        """Visit while statement"""
        cond_type = self.visit(node.condition)
        if cond_type and not TypeChecker.is_numeric_type(cond_type):
            self.warning(f"Using non-numeric type '{cond_type}' in condition", node)
        
        self.loop_depth += 1
        self.visit(node.body)
        self.loop_depth -= 1
    
    def visit_ForStmt(self, node):
        """Visit for statement"""
        self.enter_scope()  # For loop creates its own scope
        
        if node.init:
            self.visit(node.init)
        
        if node.condition:
            cond_type = self.visit(node.condition)
            if cond_type and not TypeChecker.is_numeric_type(cond_type):
                self.warning(f"Using non-numeric type '{cond_type}' in condition", node)
        
        if node.update:
            self.visit(node.update)
        
        self.loop_depth += 1
        self.visit(node.body)
        self.loop_depth -= 1
        
        self.exit_scope()
    
    def visit_ReturnStmt(self, node):
        """Visit return statement"""
        if not self.current_function:
            self.error("Return statement outside function", node)
            return
        
        expected_type = self._get_type_string(self.current_function.return_type)
        
        if node.value:
            actual_type = self.visit(node.value)
            if actual_type and not TypeChecker.can_convert(actual_type, expected_type):
                self.error(f"Cannot convert return value from '{actual_type}' to '{expected_type}'", node)
        elif expected_type != 'void':
            self.warning(f"Non-void function should return a value", node)
    
    def visit_BreakStmt(self, node):
        """Visit break statement"""
        if self.loop_depth == 0:
            self.error("Break statement not within loop", node)
    
    def visit_ContinueStmt(self, node):
        """Visit continue statement"""
        if self.loop_depth == 0:
            self.error("Continue statement not within loop", node)
    
    def visit_BinaryOp(self, node):
        """Visit binary operation"""
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        if not left_type or not right_type:
            return None
        
        # Type checking for different operators
        if node.operator in ['+', '-', '*', '/', '%']:
            if not TypeChecker.is_numeric_type(left_type) or not TypeChecker.is_numeric_type(right_type):
                self.error(f"Invalid operands to binary '{node.operator}' (have '{left_type}' and '{right_type}')", node)
                return None
            
            if node.operator == '%' and (TypeChecker.is_floating_type(left_type) or TypeChecker.is_floating_type(right_type)):
                self.error("Invalid operands to binary '%' (floating point types)", node)
                return None
            
            return TypeChecker.promote_types(left_type, right_type)
        
        elif node.operator in ['<', '>', '<=', '>=', '==', '!=']:
            if not TypeChecker.can_convert(left_type, right_type) and not TypeChecker.can_convert(right_type, left_type):
                self.error(f"Invalid operands to binary '{node.operator}'", node)
            return 'int'  # Comparison results in int
        
        elif node.operator in ['&&', '||']:
            return 'int'  # Logical operations result in int
        
        elif node.operator in ['&', '|', '^', '<<', '>>']:
            if not TypeChecker.is_integer_type(left_type) or not TypeChecker.is_integer_type(right_type):
                self.error(f"Invalid operands to binary '{node.operator}' (need integer types)", node)
            return TypeChecker.promote_types(left_type, right_type)
        
        return None
    
    def visit_UnaryOp(self, node):
        """Visit unary operation"""
        operand_type = self.visit(node.operand)
        
        if not operand_type:
            return None
        
        if node.operator in ['++', '--']:
            if not TypeChecker.is_numeric_type(operand_type):
                self.error(f"Invalid operand to unary '{node.operator}'", node)
            return operand_type
        
        elif node.operator in ['+', '-']:
            if not TypeChecker.is_numeric_type(operand_type):
                self.error(f"Invalid operand to unary '{node.operator}'", node)
            return operand_type
        
        elif node.operator == '!':
            return 'int'
        
        elif node.operator == '~':
            if not TypeChecker.is_integer_type(operand_type):
                self.error(f"Invalid operand to unary '~' (need integer type)", node)
            return operand_type
        
        elif node.operator == '&':  # Address-of
            return f"{operand_type}*"
        
        elif node.operator == '*':  # Dereference
            if not operand_type.endswith('*'):
                self.error("Invalid type argument of unary '*'", node)
                return None
            return operand_type[:-1]  # Remove *
        
        return operand_type
    
    def visit_AssignmentExpr(self, node):
        """Visit assignment expression"""
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        if not left_type or not right_type:
            return left_type
        
        if node.operator == '=':
            if not TypeChecker.can_convert(right_type, left_type):
                self.error(f"Cannot convert '{right_type}' to '{left_type}' in assignment", node)
        else:
            # Compound assignment operators
            op = node.operator[:-1]  # Remove '='
            if op in ['+', '-', '*', '/', '%']:
                if not TypeChecker.is_numeric_type(left_type) or not TypeChecker.is_numeric_type(right_type):
                    self.error(f"Invalid operands to '{node.operator}'", node)
        
        return left_type
    
    def visit_FunctionCall(self, node):
        """Visit function call"""
        func_name = node.function.name if isinstance(node.function, Identifier) else str(node.function)
        
        # Look up function
        func_symbol = self.current_scope.lookup(func_name)
        if not func_symbol:
            self.error(f"Undefined function '{func_name}'", node)
            return None
        
        if func_symbol.symbol_type != 'function':
            self.error(f"'{func_name}' is not a function", node)
            return None
        
        # Check argument count
        expected_params = len(func_symbol.parameters)
        actual_args = len(node.arguments)
        
        # Handle variadic functions (like printf)
        if func_name in ['printf', 'scanf']:
            if actual_args < 1:
                self.error(f"Too few arguments to function '{func_name}'", node)
        elif actual_args != expected_params:
            self.error(f"Wrong number of arguments to function '{func_name}' (expected {expected_params}, got {actual_args})", node)
        
        # Type check arguments
        for i, arg in enumerate(node.arguments):
            arg_type = self.visit(arg)
            if i < len(func_symbol.parameters) and arg_type:
                param_type = self._get_type_string(func_symbol.parameters[i].param_type)
                if not TypeChecker.can_convert(arg_type, param_type):
                    self.error(f"Cannot convert argument {i+1} from '{arg_type}' to '{param_type}'", node)
        
        return func_symbol.data_type
    
    def visit_Identifier(self, node):
        """Visit identifier"""
        symbol = self.current_scope.lookup(node.name)
        if not symbol:
            self.error(f"Undefined identifier '{node.name}'", node)
            return None
        
        return symbol.data_type
    
    def visit_IntegerLiteral(self, node):
        """Visit integer literal"""
        return 'int'
    
    def visit_FloatLiteral(self, node):
        """Visit float literal"""
        return 'double'  # Default for floating literals
    
    def visit_CharLiteral(self, node):
        """Visit character literal"""
        return 'char'
    
    def visit_StringLiteral(self, node):
        """Visit string literal"""
        return 'char*'
    
    def visit_ExpressionInitializer(self, node):
        """Visit expression initializer"""
        return self.visit(node.expression)
    
    def _get_type_string(self, type_node):
        """Convert type node to string representation"""
        if isinstance(type_node, str):
            return type_node
        elif isinstance(type_node, BasicType):
            return type_node.type_name
        elif isinstance(type_node, PointerType):
            base_type = self._get_type_string(type_node.base_type)
            return f"{base_type}*"
        elif isinstance(type_node, ArrayType):
            base_type = self._get_type_string(type_node.base_type)
            return f"{base_type}[]"
        else:
            return str(type_node)
    
    def _compatible_function_signatures(self, existing_symbol, new_function):
        """Check if function signatures are compatible"""
        if existing_symbol.data_type != self._get_type_string(new_function.return_type):
            return False
        
        if len(existing_symbol.parameters) != len(new_function.parameters):
            return False
        
        for existing_param, new_param in zip(existing_symbol.parameters, new_function.parameters):
            if self._get_type_string(existing_param.param_type) != self._get_type_string(new_param.param_type):
                return False
        
        return True

def analyze_semantics(ast):
    """Convenience function to perform semantic analysis"""
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    return success, analyzer.errors, analyzer.warnings
