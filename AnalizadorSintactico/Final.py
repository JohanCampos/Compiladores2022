
from Buffer import Buffer
from AnalizadorLexico import AnalizadorLexico
from Token import Token

def error(id, terminal, esperado):
    #tabla Error
    #id = 1: Se esperaba un terminal y recibio uno distinto
    print('Hubo un error en la sintaxis')
    if id == 1:
        print('Recibio un '+terminal+', se esperaba un '+str(esperado)+'.')

def coincidir(esperado, avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == esperado:
        return avance + 1 
    else:
        error(1,terminal,esperado)
        return -1

def Param(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = coincidir('INT', avance, token)
        avance = coincidir('ID', avance, token)
        avance = ParamsPrima(avance, token)
        return avance
    elif terminal == 'FLOAT':
        avance = coincidir('FLOAT', avance, token)
        avance = coincidir('ID', avance, token)
        return avance
    elif terminal == 'CHAR':
        avance = coincidir('CHAR', avance, token)
        avance = coincidir('ID', avance, token)
        return avance
    else:
        error(1,terminal,['INT','FLOAT','CHAR','VOID'])

def Params(avance,token):
    avance = Param(avance, token)
    

def Funcs(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'PARENTESIS_APERTURA':
        avance = coincidir('PARENTESIS_APERTURA', avance, token)
        avance = Params(avance, token)
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)
    else:
        error(1,terminal,'PARENTESIS_APERTURA')

def program(avance, token):
    terminal = token[avance].getNombreToken()
    #TypeSpec
    if terminal == 'INT':
        return
    elif terminal == 'FLOAT':
        return
    elif terminal == 'CHAR':
        return
    #VOID
    elif terminal == 'VOID':
        avance = coincidir('VOID', avance, token)
        avance = coincidir('ID', avance, token)
        
    else:
        error(1,terminal,['INT','FLOAT','CHAR','VOID'])

if __name__ == '__main__':
    Buffer = Buffer()
    Analizador = AnalizadorLexico()
    token = Token()
    

    # Lista de cada lista devuelta por la función tokenize
    #token = []
    #lexema = []
    #fila = []
    #columna = []

    # Obtenemos los tokens y recargams el buffer
    for i in Buffer.load_buffer():
        token = Analizador.tokenize(i)
        """token += t
        lexema += lex
        fila += lin
        columna += col
        """
    avance = 0
    program(avance, token)
    ##print('\nTokens reconocidos: ', token)

