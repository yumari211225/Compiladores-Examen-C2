# parser_1.py
import ply.yacc as yacc
from lexer import tokens, lexer

defined_variables = {}
initial_values = {}
loop_variables = set()  # Conjunto adicional para almacenar variables definidas en bucles

def p_program(p):
    '''program : declarations statements'''
    validate_variables()
    p[0] = "La estructura del código está bien."

def p_declarations(p):
    '''declarations : declarations declaration
                    | declaration'''

def p_declaration(p):
    '''declaration : INT ID ASSIGN NUMBER SEMICOLON
                   | FLOAT ID ASSIGN FLOAT_LITERAL SEMICOLON
                   | STRING ID ASSIGN STRING_LITERAL SEMICOLON'''
    defined_variables[p[2]] = p[1]  # Guardar el tipo de la variable
    initial_values[p[2]] = p[4]  # Guardar el valor inicial de la variable

def p_statements(p):
    '''statements : statements statement
                  | statement'''

def p_statement(p):
    '''statement : if_statement
                 | while_statement
                 | for_statement
                 | input_statement
                 | increment_statement
                 | assignment_statement'''

def p_if_statement(p):
    '''if_statement : IF LPAREN condition RPAREN LBRACE statements RBRACE'''

def p_condition(p):
    '''condition : expression AND expression
                 | expression'''
    p[0] = p[1]

def p_expression(p):
    '''expression : simple_expression comparison_operator simple_expression
                  | simple_expression'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = (p[2], p[1], p[3])

def p_simple_expression(p):
    '''simple_expression : ID
                         | NUMBER
                         | FLOAT_LITERAL
                         | STRING_LITERAL'''
    if isinstance(p[1], str) and p.slice[1].type == 'ID':
        validate_variable_definition(p[1])
    p[0] = p[1]

def p_comparison_operator(p):
    '''comparison_operator : EQ
                           | GT
                           | GE
                           | LT
                           | LE
                           | NE'''
    p[0] = p[1]

def p_while_statement(p):
    '''while_statement : WHILE LPAREN condition RPAREN LBRACE statements RBRACE'''

def p_for_statement(p):
    '''for_statement : FOR LPAREN ID IN RANGE LPAREN NUMBER COMMA NUMBER RPAREN RPAREN LBRACE statements RBRACE'''
    loop_variables.add(p[3])  # Agregar variable del bucle for al conjunto de variables definidas en bucles
    validate_variable_definition(p[3])
    p[0] = f"For loop con variable {p[3]} en rango ({p[6]}, {p[8]})"

def p_input_statement(p):
    '''input_statement : INPUT LPAREN simple_expression RPAREN SEMICOLON'''
    if not isinstance(p[3], str):
        raise ValueError(f"Error semántico: La función input debe recibir una cadena, encontrado {p[3]}.")

def p_increment_statement(p):
    '''increment_statement : ID PLUS PLUS SEMICOLON'''
    validate_variable_definition(p[1])

def p_assignment_statement(p):
    '''assignment_statement : ID ASSIGN expression SEMICOLON'''
    validate_variable_definition(p[1])
    if p[1] == 'B':
        if p[3] != initial_values['B']:
            raise ValueError(f"Error semántico en línea {p.lineno(1)}: Variable 'B' debe mantener el valor {initial_values['B']}.")

def validate_variable_definition(variable):
    if variable not in defined_variables and variable not in loop_variables:
        raise ValueError(f"Error semántico: Variable '{variable}' no definida correctamente.")

def validate_variables():
    pass

def p_error(p):
    if p:
        error_message = f"Línea {p.lineno}.- Error de sintaxis en '{p.value}'"
        raise SyntaxError(error_message)
    else:
        # Aquí usamos lexer.lineno en lugar de lexer.lexer.lineno
        raise SyntaxError(f"Error de sintaxis al final del archivo en la línea {lexer.lineno}. Falta una llave de cierre o punto y coma.")

parser = yacc.yacc()

def parse_semantic(code):
    global defined_variables, loop_variables, initial_values
    defined_variables = {}
    loop_variables = set()
    initial_values = {}
    lexer.lineno = 1
    try:
        result = parser.parse(code, lexer=lexer)
        return result if result else 'La estructura del código está bien'
    except (SyntaxError, ValueError) as e:
        raise e

def parse_code(code):
    global defined_variables, loop_variables, initial_values
    defined_variables = {}
    loop_variables = set()
    initial_values = {}
    lexer.lineno = 1
    try:
        result = parser.parse(code, lexer=lexer)
        return result if result else "La estructura del código está bien."
    except (SyntaxError, ValueError) as e:
        raise e
