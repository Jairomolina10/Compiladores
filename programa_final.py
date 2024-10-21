import re
import sys
import ply.lex as lex
import ply.yacc as yacc
import matplotlib.pyplot as plt

# Definición de tokens para el analizador léxico
token_specification = [
    ('NUMEROS', r'\d+(\.\d*)?'),
    ('DELIMITADORES', r'[""\=(){}:;,.#]'),
    ('IDENTIFICADORES', r'[A-Za-z_]\w*'),
    ('OPERADORES', r'[+\-*/%]'),
    ('NUEVALINEA', r'\n'),
    ('SKIP', r'[ \t]+'),
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
        elif kind == 'IDENTIFICADORES' and value in {'if', 'elif', 'else', 'for', 'range', 'in', 'while', 'return', 'break', 'function', 'int', 'double', 'float', 'import', 'input', 'print'}:
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

def dibujar_arbol(nodo, x=0, y=0, layer=1):
    """ Dibuja un árbol sintáctico en un gráfico utilizando matplotlib. """
    if isinstance(nodo, tuple):
        # Dibuja el nodo
        plt.text(x, y, str(nodo[0]), ha='center', va='center', fontsize=16 + layer, bbox=dict(boxstyle='round,pad=0.4', edgecolor='black', facecolor='lightgray'))

        # Ajuste para las posiciones de los hijos
        offset = 1 / (2 ** layer)  # Espaciado entre nodos
        # Dibuja el hijo izquierdo
        if isinstance(nodo[1], tuple) or isinstance(nodo[1], (int, float)):
            plt.plot([x, x - offset], [y, y - 1], color='black')  # Línea hacia el hijo izquierdo
            dibujar_arbol(nodo[1], x - offset, y - 1, layer + 1)
        # Dibuja el hijo derecho
        if isinstance(nodo[2], tuple) or isinstance(nodo[2], (int, float)):
            plt.plot([x, x + offset], [y, y - 1], color='black')  # Línea hacia el hijo derecho
            dibujar_arbol(nodo[2], x + offset, y - 1, layer + 1)
    else:
        # Dibuja el valor del nodo
        plt.text(x, y, str(nodo), ha='center', va='center', fontsize=16, bbox=dict(boxstyle='round,pad=0.4', edgecolor='black', facecolor='lightgreen'))

def generar_arbol(codigo):
    try:
        resultado = parser.parse(codigo)
        if resultado:
            print("Árbol sintáctico generado:")
            plt.figure(figsize=(14, 12))  # Ajusta el tamaño de la figura
            plt.title("Árbol Sintáctico", fontsize=20)
            plt.axis('off')  # No mostrar los ejes
            dibujar_arbol(resultado)  # Dibuja el árbol
            plt.show()  # Muestra el gráfico
        else:
            print("Error: no se pudo generar el árbol sintáctico.")
    except Exception as e:
        print(f"Error: {e}")

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

