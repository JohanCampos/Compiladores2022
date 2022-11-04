
from Buffer import Buffer
from AnalizadorLexico import AnalizadorLexico

if __name__ == '__main__':
    Buffer = Buffer()
    Analizador = AnalizadorLexico()

    # Lista de cada lista devuelta por la función tokenize
    token = []
    lexema = []
    fila = []
    columna = []

    # Obtenemos los tokens y recargams el buffer
    for i in Buffer.load_buffer():
        t, lex, lin, col = Analizador.tokenize(i)
        token += t
        lexema += lex
        fila += lin
        columna += col

    print('\nTokens reconocidos: ', token)

