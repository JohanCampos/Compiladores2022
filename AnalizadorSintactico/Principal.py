
from Buffer import Buffer
from AnalizadorLexico import AnalizadorLexico
from Token import Token
from AnalizadorSintactico import AnalizadorSintactico

if __name__ == '__main__':
    Buffer = Buffer()
    Analizador = AnalizadorLexico()
    token = Token()
    Sintactico = AnalizadorSintactico()

    # Lista de cada lista devuelta por la función tokenize
    #token = []
    #lexema = []
    #fila = []
    #columna = []

    # Obtenemos los tokens y recargams el buffer
    for i in Buffer.load_buffer():
        token = Analizador.tokenize(i)
        Sintactico.inicial(token)
        """token += t
        lexema += lex
        fila += lin
        columna += col
        """
    ##print('\nTokens reconocidos: ', token)

