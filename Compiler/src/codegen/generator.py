#!/usr/bin/env python3

"""
Code Generator for C-like Language
Generates x86 assembly code from validated AST
"""

try:
    from ..parser.ast_nodes import *
    from ..semantic.analyzer import TypeChecker
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'parser'))
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'semantic'))
    from ast_nodes import *
    from analyzer import TypeChecker

class CodeGenerator:
    """Code generator for C-like language assembly output"""
    
    def __init__(self):
        self.code = []
        self.data_section = []
        self.bss_section = []
        self.label_counter = 0
        self.string_literals = {}
        self.current_function = None
        self.stack_offset = 0
        self.local_vars = {}
        self.function_signatures = {}
    
    def generate(self, ast):
        """Generate assembly code from AST"""
        self.code = []
        self.data_section = []
        self.bss_section = []
        
        # Generate header
        self._generate_header()
        
        # Handle Program node - check if it has declarations attribute
        if hasattr(ast, 'declarations') and ast.declarations:
            # Process all declarations in the program
            for node in ast.declarations:
                self._generate_node(node)
        elif hasattr(ast, 'external_declarations') and ast.external_declarations:
            # Handle TranslationUnit
            for node in ast.external_declarations:
                self._generate_node(node)
        else:
            # Single node or simple case
            self._generate_node(ast)
        
        # Generate complete assembly
        return self._build_complete_assembly()
    
    def _generate_header(self):
        """Generate assembly header"""
        self.code.extend([
            "; C-like Language Compiler Output",
            "; Supports function calls and all C data types",
            "",
            "section .text",
            "global _start",
            ""
        ])
    
    def _generate_node(self, node):
        """Generate code for any AST node"""
        method_name = f"_generate_{type(node).__name__.lower()}"
        method = getattr(self, method_name, self._generate_default)
        return method(node)
    
    def _generate_program(self, node):
        """Generate code for program node"""
        for child in node.children:
            self._generate_node(child)
    
    def _generate_functiondefinition(self, node):
        """Generate code for function definition"""
        func_name = node.name
        self.current_function = func_name
        self.stack_offset = 0
        self.local_vars = {}
        
        # Function label
        if func_name == "main":
            self.code.append("_start:")
        else:
            self.code.append(f"{func_name}:")
        
        # Function prologue
        self.code.extend([
            "    push ebp",
            "    mov ebp, esp"
        ])
        
        # Process parameters
        param_offset = 8  # Start after return address and saved ebp
        for param in node.parameters:
            param_name = param.declarator.name if hasattr(param.declarator, 'name') else str(param.declarator)
            self.local_vars[param_name] = param_offset
            param_offset += self._get_type_size(param.type_spec)
        
        # Generate function body
        if node.body:
            self._generate_node(node.body)
        
        # Function epilogue (if no explicit return)
        if func_name == "main":
            self.code.extend([
                "    mov eax, 1      ; sys_exit",
                "    mov ebx, 0      ; exit status",
                "    int 0x80        ; system call"
            ])
        else:
            self.code.extend([
                "    mov esp, ebp",
                "    pop ebp",
                "    ret"
            ])
        
        self.code.append("")
        self.current_function = None
    
    def _generate_variabledeclaration(self, node):
        """Generate code for variable declaration"""
        var_name = node.declarator.name if hasattr(node.declarator, 'name') else str(node.declarator)
        type_size = self._get_type_size(node.type_spec)
        
        if self.current_function:
            # Local variable
            self.stack_offset += type_size
            self.local_vars[var_name] = -self.stack_offset
            
            # Initialize if there's an initializer
            if node.initializer:
                self._generate_node(node.initializer)
                self.code.append(f"    mov [ebp{self.local_vars[var_name]:+d}], eax")
        else:
            # Global variable
            if node.initializer:
                # Initialized global
                init_value = self._evaluate_constant(node.initializer)
                self.data_section.append(f"{var_name}: dd {init_value}")
            else:
                # Uninitialized global
                self.bss_section.append(f"{var_name}: resd 1")
    
    def _generate_compoundstatement(self, node):
        """Generate code for compound statement (block)"""
        for stmt in node.statements:
            self._generate_node(stmt)
    
    def _generate_ifstatement(self, node):
        """Generate code for if statement"""
        else_label = self._new_label("else")
        end_label = self._new_label("end_if")
        
        # Generate condition
        self._generate_node(node.condition)
        self.code.extend([
            "    cmp eax, 0",
            f"    je {else_label}"
        ])
        
        # Generate then statement
        self._generate_node(node.then_statement)
        self.code.append(f"    jmp {end_label}")
        
        # Generate else statement
        self.code.append(f"{else_label}:")
        if node.else_statement:
            self._generate_node(node.else_statement)
        
        self.code.append(f"{end_label}:")
    
    def _generate_whilestatement(self, node):
        """Generate code for while statement"""
        start_label = self._new_label("while_start")
        end_label = self._new_label("while_end")
        
        self.code.append(f"{start_label}:")
        
        # Generate condition
        self._generate_node(node.condition)
        self.code.extend([
            "    cmp eax, 0",
            f"    je {end_label}"
        ])
        
        # Generate body
        self._generate_node(node.body)
        self.code.append(f"    jmp {start_label}")
        
        self.code.append(f"{end_label}:")
    
    def _generate_forstatement(self, node):
        """Generate code for for statement"""
        start_label = self._new_label("for_start")
        continue_label = self._new_label("for_continue")
        end_label = self._new_label("for_end")
        
        # Generate initialization
        if node.init:
            self._generate_node(node.init)
        
        self.code.append(f"{start_label}:")
        
        # Generate condition
        if node.condition:
            self._generate_node(node.condition)
            self.code.extend([
                "    cmp eax, 0",
                f"    je {end_label}"
            ])
        
        # Generate body
        self._generate_node(node.body)
        
        self.code.append(f"{continue_label}:")
        
        # Generate update
        if node.update:
            self._generate_node(node.update)
        
        self.code.append(f"    jmp {start_label}")
        self.code.append(f"{end_label}:")
    
    def _generate_returnstatement(self, node):
        """Generate code for return statement"""
        if node.expression:
            self._generate_node(node.expression)
        else:
            self.code.append("    mov eax, 0")
        
        if self.current_function == "main":
            self.code.extend([
                "    mov ebx, eax    ; exit status",
                "    mov eax, 1      ; sys_exit",
                "    int 0x80        ; system call"
            ])
        else:
            self.code.extend([
                "    mov esp, ebp",
                "    pop ebp", 
                "    ret"
            ])
    
    def _generate_expressionstatement(self, node):
        """Generate code for expression statement"""
        if node.expression:
            self._generate_node(node.expression)
    
    def _generate_functioncall(self, node):
        """Generate code for function call"""
        func_name = node.function.name if hasattr(node.function, 'name') else str(node.function)
        
        # Handle built-in functions
        if func_name == "printf":
            self._generate_printf_call(node)
            return
        elif func_name == "scanf":
            self._generate_scanf_call(node)
            return
        
        # Push arguments in reverse order (right to left)
        for arg in reversed(node.arguments):
            self._generate_node(arg)
            self.code.append("    push eax")
        
        # Call function
        self.code.append(f"    call {func_name}")
        
        # Clean up stack (remove arguments)
        if node.arguments:
            stack_cleanup = len(node.arguments) * 4  # Assuming 4 bytes per argument
            self.code.append(f"    add esp, {stack_cleanup}")
    
    def _generate_printf_call(self, node):
        """Generate code for printf function call"""
        if not node.arguments:
            return
        
        format_str = node.arguments[0]
        if isinstance(format_str, StringLiteral):
            # Store format string
            str_label = self._store_string_literal(format_str.value)
            
            # Push arguments in reverse order
            for arg in reversed(node.arguments[1:]):
                self._generate_node(arg)
                self.code.append("    push eax")
            
            # Push format string
            self.code.extend([
                f"    push {str_label}",
                "    call printf",
                f"    add esp, {len(node.arguments) * 4}"
            ])
    
    def _generate_scanf_call(self, node):
        """Generate code for scanf function call"""
        if len(node.arguments) < 2:
            return
        
        format_str = node.arguments[0]
        if isinstance(format_str, StringLiteral):
            str_label = self._store_string_literal(format_str.value)
            
            # Push variable addresses
            for arg in reversed(node.arguments[1:]):
                if isinstance(arg, Identifier):
                    var_name = arg.name
                    if var_name in self.local_vars:
                        self.code.append(f"    lea eax, [ebp{self.local_vars[var_name]:+d}]")
                    else:
                        self.code.append(f"    mov eax, {var_name}")
                    self.code.append("    push eax")
            
            self.code.extend([
                f"    push {str_label}",
                "    call scanf",
                f"    add esp, {len(node.arguments) * 4}"
            ])
    
    def _generate_binaryoperation(self, node):
        """Generate code for binary operation"""
        # Generate right operand first (will be in eax)
        self._generate_node(node.right)
        self.code.append("    push eax")
        
        # Generate left operand (will be in eax)
        self._generate_node(node.left)
        self.code.append("    pop ebx")  # Right operand now in ebx
        
        # Perform operation
        if node.operator == '+':
            self.code.append("    add eax, ebx")
        elif node.operator == '-':
            self.code.append("    sub eax, ebx")
        elif node.operator == '*':
            self.code.append("    imul eax, ebx")
        elif node.operator == '/':
            self.code.extend([
                "    cdq",           # Sign extend eax into edx:eax
                "    idiv ebx"       # Result in eax, remainder in edx
            ])
        elif node.operator == '%':
            self.code.extend([
                "    cdq",
                "    idiv ebx",
                "    mov eax, edx"   # Move remainder to eax
            ])
        elif node.operator == '==':
            self._generate_comparison("sete")
        elif node.operator == '!=':
            self._generate_comparison("setne")
        elif node.operator == '<':
            self._generate_comparison("setl")
        elif node.operator == '<=':
            self._generate_comparison("setle")
        elif node.operator == '>':
            self._generate_comparison("setg")
        elif node.operator == '>=':
            self._generate_comparison("setge")
        elif node.operator == '&&':
            self._generate_logical_and()
        elif node.operator == '||':
            self._generate_logical_or()
        elif node.operator == '&':
            self.code.append("    and eax, ebx")
        elif node.operator == '|':
            self.code.append("    or eax, ebx")
        elif node.operator == '^':
            self.code.append("    xor eax, ebx")
        elif node.operator == '<<':
            self.code.extend([
                "    mov ecx, ebx",
                "    shl eax, cl"
            ])
        elif node.operator == '>>':
            self.code.extend([
                "    mov ecx, ebx",
                "    sar eax, cl"
            ])
    
    def _generate_comparison(self, set_instruction):
        """Generate comparison operation"""
        self.code.extend([
            "    cmp eax, ebx",
            f"    {set_instruction} al",
            "    movzx eax, al"
        ])
    
    def _generate_logical_and(self):
        """Generate logical AND operation"""
        false_label = self._new_label("and_false")
        end_label = self._new_label("and_end")
        
        self.code.extend([
            "    cmp eax, 0",
            f"    je {false_label}",
            "    cmp ebx, 0",
            f"    je {false_label}",
            "    mov eax, 1",
            f"    jmp {end_label}",
            f"{false_label}:",
            "    mov eax, 0",
            f"{end_label}:"
        ])
    
    def _generate_logical_or(self):
        """Generate logical OR operation"""
        true_label = self._new_label("or_true")
        end_label = self._new_label("or_end")
        
        self.code.extend([
            "    cmp eax, 0",
            f"    jne {true_label}",
            "    cmp ebx, 0",
            f"    jne {true_label}",
            "    mov eax, 0",
            f"    jmp {end_label}",
            f"{true_label}:",
            "    mov eax, 1",
            f"{end_label}:"
        ])
    
    def _generate_unaryoperation(self, node):
        """Generate code for unary operation"""
        self._generate_node(node.operand)
        
        if node.operator == '-':
            self.code.append("    neg eax")
        elif node.operator == '+':
            # Unary plus does nothing
            pass
        elif node.operator == '!':
            self.code.extend([
                "    cmp eax, 0",
                "    sete al",
                "    movzx eax, al"
            ])
        elif node.operator == '~':
            self.code.append("    not eax")
        elif node.operator == '++':
            if isinstance(node.operand, Identifier):
                var_name = node.operand.name
                if var_name in self.local_vars:
                    self.code.extend([
                        f"    inc dword [ebp{self.local_vars[var_name]:+d}]",
                        f"    mov eax, [ebp{self.local_vars[var_name]:+d}]"
                    ])
                else:
                    self.code.extend([
                        f"    inc dword [{var_name}]",
                        f"    mov eax, [{var_name}]"
                    ])
        elif node.operator == '--':
            if isinstance(node.operand, Identifier):
                var_name = node.operand.name
                if var_name in self.local_vars:
                    self.code.extend([
                        f"    dec dword [ebp{self.local_vars[var_name]:+d}]",
                        f"    mov eax, [ebp{self.local_vars[var_name]:+d}]"
                    ])
                else:
                    self.code.extend([
                        f"    dec dword [{var_name}]",
                        f"    mov eax, [{var_name}]"
                    ])
    
    def _generate_assignment(self, node):
        """Generate code for assignment"""
        # Generate right-hand side
        self._generate_node(node.right)
        
        # Store in left-hand side
        if isinstance(node.left, Identifier):
            var_name = node.left.name
            if var_name in self.local_vars:
                self.code.append(f"    mov [ebp{self.local_vars[var_name]:+d}], eax")
            else:
                self.code.append(f"    mov [{var_name}], eax")
    
    def _generate_identifier(self, node):
        """Generate code for identifier (variable reference)"""
        var_name = node.name
        if var_name in self.local_vars:
            self.code.append(f"    mov eax, [ebp{self.local_vars[var_name]:+d}]")
        else:
            self.code.append(f"    mov eax, [{var_name}]")
    
    def _generate_integerliteral(self, node):
        """Generate code for integer literal"""
        self.code.append(f"    mov eax, {node.value}")
    
    def _generate_floatliteral(self, node):
        """Generate code for float literal"""
        # Store float in data section and load it
        float_label = self._new_label("float")
        self.data_section.append(f"{float_label}: dd {node.value}")
        self.code.append(f"    mov eax, [{float_label}]")
    
    def _generate_stringliteral(self, node):
        """Generate code for string literal"""
        str_label = self._store_string_literal(node.value)
        self.code.append(f"    mov eax, {str_label}")
    
    def _generate_charliteral(self, node):
        """Generate code for character literal"""
        self.code.append(f"    mov eax, {ord(node.value)}")
    
    def _generate_default(self, node):
        """Default handler for unimplemented nodes"""
        self.code.append(f"    ; TODO: Implement {type(node).__name__}")
    
    def _store_string_literal(self, string_value):
        """Store string literal in data section"""
        if string_value not in self.string_literals:
            label = self._new_label("str")
            # Escape string and null-terminate
            escaped = string_value.replace('\\n', '", 10, "').replace('\\t', '", 9, "')
            self.data_section.append(f'{label}: db "{escaped}", 0')
            self.string_literals[string_value] = label
        return self.string_literals[string_value]
    
    def _get_type_size(self, type_spec):
        """Get size of a type in bytes"""
        if isinstance(type_spec, BasicType):
            type_name = type_spec.type_name
        else:
            type_name = str(type_spec)
        
        size_map = {
            'char': 1, 'signed char': 1, 'unsigned char': 1,
            'short': 2, 'signed short': 2, 'unsigned short': 2,
            'int': 4, 'signed int': 4, 'unsigned int': 4,
            'long': 4, 'signed long': 4, 'unsigned long': 4,
            'float': 4, 'double': 8, 'long double': 10,
            'void*': 4  # Pointer size
        }
        return size_map.get(type_name, 4)  # Default to 4 bytes
    
    def _evaluate_constant(self, node):
        """Evaluate constant expression for initialization"""
        if isinstance(node, IntegerLiteral):
            return node.value
        elif isinstance(node, FloatLiteral):
            return node.value
        elif isinstance(node, CharLiteral):
            return ord(node.value)
        else:
            return 0  # Default value
    
    def _new_label(self, prefix="label"):
        """Generate a new unique label"""
        self.label_counter += 1
        return f"{prefix}_{self.label_counter}"
    
    def _build_complete_assembly(self):
        """Build the complete assembly output"""
        result = []
        
        # Data section
        if self.data_section:
            result.extend([
                "section .data",
                *self.data_section,
                ""
            ])
        
        # BSS section
        if self.bss_section:
            result.extend([
                "section .bss",
                *self.bss_section,
                ""
            ])
        
        # Text section
        result.extend([
            "section .text",
            "global _start",
            ""
        ])
        
        # Add external function declarations
        if any("printf" in line for line in self.code):
            result.extend([
                "extern printf",
                ""
            ])
        if any("scanf" in line for line in self.code):
            result.extend([
                "extern scanf",
                ""
            ])
        
        # Add generated code
        result.extend(self.code)
        
        return '\n'.join(result)
