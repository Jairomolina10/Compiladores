import ply.lex as lex
import ply.yacc as yacc

# Definición de tokens para el lexer
tokens = (
    'NUMEROS',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'PARENTESIS_IZQUIERDO',
    'PARENTESIS_DERECHO',
)

# Expresiones regulares para cada token
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_PARENTESIS_IZQUIERDO = r'\('
t_PARENTESIS_DERECHO = r'\)'

# Regla para reconocer números
def t_NUMEROS(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para ignorar espacios
t_ignore = ' \t'

# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal: {t.value[0]}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Definición de reglas gramaticales para el parser
def p_expression_binop(p):
    '''expression : expression SUMA term
                  | expression RESTA term'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_binop(p):
    '''term : term MULTIPLICACION factor
            | term DIVISION factor'''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMEROS'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : PARENTESIS_IZQUIERDO expression PARENTESIS_DERECHO'
    p[0] = p[2]

# Manejo de errores sintácticos
def p_error(p):
    print("Error de sintaxis")

# Construir el parser
parser = yacc.yacc()

# Función para analizar código
def analizar_codigo(codigo):
    try:
        result = parser.parse(codigo)
        print(f"Resultado: {result}")
    except Exception as e:
        print(f"Error: {e}")

# Ejemplo 
codigo = "3 + 5 * 10 - 4 )"
analizar_codigo(codigo)
