import re
import sys

#Se definen los tokens

token_specification = [
    ('NUMEROS',   r'\d+(\.\d*)?'),                   # Números enteros o decimales
    ('DELIMITADORES',   r'[""\=(){}:;,.#]'),         # Operador de asignación "="
    ('IDENTIFICADORES',       r'[A-Za-z_]\w*'),      # Identificadores (nombres de variables y funciones)
    ('OPERADORES',       r'[+\-*/%]'),               # Operadores aritméticos "+", "-", "*", "/"
    ('NUEVALINEA',  r'\n'),                          # Saltos de línea "\n"
    ('SKIP',     r'[ \t]+'),                         # Espacios y tabulaciones (se ignoran)
    ('MISMATCH', r'.'),                              # Cualquier otro carácter no esperado
]
token_re = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification) #Toma la linea de codigo e identifica cada uno de sus componentes y los compara con los tokens

def analizador(codigo):
    tokens = []
    line_num = 1
    line_start = 0

    for match in re.finditer(token_re, codigo): #Se reconocen las coincidencias en el codigo con los tokens
        kind = match.lastgroup    #Clasifica las coincidencias
        value = match.group()     #Guarda los valores
        column = match.start() - line_start     #Guarda la posicion del token

        if kind == 'NUMEROS':
            value = float(value) if '.' in value else int(value)
        elif kind == 'IDENTIFICADORES' and value in {'if','elif', 'else','for','range','in', 'while', 'return','break', 'function','int','double','float','import','input','print'}:
             kind = 'PALABRA_CLAVE'  # Identificamos palabras clave
        elif kind == 'NUEVALINEA':
            line_start = match.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue  # Ignoramos espacios y tabulaciones
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} inesperado en la línea {line_num}')

        tokens.append((kind, value, line_num, column))

    return tokens

def main():
    print("Bienvenido al Analizador Léxico Interactivo\n")
    print("Escribe el código que deseas analizar y presiona 'Ctrl+Z + enter' cuando termines:\n")
    
    codigo = sys.stdin.read() 
    
    print("\nAnalizando...\n")
    tokens = analizador(codigo)
    
    print("\nResumen de Tokens:")
    for token in tokens:
        kind, value, line_num, column = token
        print(f'Token: {value} | Tipo: {kind} | Línea: {line_num}, Columna: {column}')

    print("\nAnálisis completado. El programa se cerrará ahora.")

if __name__ == "__main__":
    main()
