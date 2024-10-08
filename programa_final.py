import re
import sys
import ply.lex as lex
import ply.yacc as yacc

# Definición de tokens para el analizador léxico
token_specification = [
    ('NUMEROS',   r'\d+(\.\d*)?'),                   
    ('DELIMITADORES',   r'[""\=(){}:;,.#]'),         
    ('IDENTIFICADORES', r'[A-Za-z_]\w*'),            
    ('OPERADORES',       r'[+\-*/%]'),               
    ('NUEVALINEA',  r'\n'),                          
    ('SKIP',     r'[ \t]+'),                         
    ('MISMATCH', r'.'),                              
]
token_re = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

# Definir el analizador léxico
def analizador(codigo):
    tokens = []
    line_num = 1
    line_start = 0
    for match in re.finditer(token_re, codigo):
        kind = match.lastgroup
        value = match.group()
        column = match.start() - line_start

        if kind == 'NUMEROS':
            value = float(value) if '.' in value else int(value)
        elif kind == 'IDENTIFICADORES' and value in {'if','elif', 'else','for','range','in', 'while', 'return','break', 'function','int','double','float','import','input','print'}:
             kind = 'PALABRA_CLAVE'
        elif kind == 'NUEVALINEA':
            line_start = match.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} inesperado en la línea {line_num}')

        tokens.append((kind, value, line_num, column))

    return tokens

# Definir tokens y gramática para el analizador sintáctico
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = ('+', p[1], p[3])

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = ('-', p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = ('*', p[1], p[3])

def p_term_divide(p):
    'term : term DIVIDE factor'
    p[0] = ('/', p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}'")
    else:
        print("Error de sintaxis al final de la entrada")

parser = yacc.yacc()

def generar_arbol(codigo):
    try:
        resultado = parser.parse(codigo)
        if resultado:
            print("Árbol sintáctico generado:")
            imprimir_arbol(resultado)
        else:
            print("Error: no se pudo generar el árbol sintáctico.")
    except Exception as e:
        print(f"Error: {e}")

def imprimir_arbol(nodo, nivel=0):
    if isinstance(nodo, tuple):
        print(' ' * nivel + str(nodo[0]))
        imprimir_arbol(nodo[1], nivel + 4)
        imprimir_arbol(nodo[2], nivel + 4)
    else:
        print(' ' * nivel + str(nodo))

# Programa principal
def main():
    print("Escribe el código que deseas analizar y presiona 'Ctrl+Z' cuando termines:")
    codigo = sys.stdin.read()  # Captura múltiples líneas de entrada
    
    # 1. Ejecutar el analizador léxico
    print("\nAnálisis Léxico:\n")
    tokens = analizador(codigo)
    for token in tokens:
        kind, value, line_num, column = token
        print(f'Token: {value} | Tipo: {kind} | Línea: {line_num}, Columna: {column}')

    # 2. Ejecutar el analizador sintáctico
    print("\nAnálisis Sintáctico (Árbol):\n")
    generar_arbol(codigo)

if __name__ == "__main__":
    main()

#codigo de ejemplo
3 + 5 * ( 10 - 4 )