
from Buffer import Buffer
from LexicalAnalyzer import LexicalAnalyzer

if __name__ == '__main__':
    Buffer = Buffer()
    Analyzer = LexicalAnalyzer()

    # Lista de cada lista devuelta por la función tokenize
    token = []
    lexeme = []
    row = []
    column = []

    # Obtenemos los tokens y recargams el buffer
    for i in Buffer.load_buffer():
        t, lex, lin, col = Analyzer.tokenize(i)
        token += t
        lexeme += lex
        row += lin
        column += col

    print('\nRecognize Tokens: ', token)

