
from Buffer import Buffer
from AnalizadorLexico import AnalizadorLexico
from Token import Token

# avance = -1 Estado de error, debe estar la primera funcion como void, para identificar entre variables y funciones

def VarDecInit(avance):
        return avance

    # numero]
def ArrayDecl(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INTEGER_CONST':
        avance = avance + 1
        terminal = token[avance].getNombreToken()
        if terminal == 'CORCHETE_CERRADURA':
            return avance + 1
        else:
            return -1
    else:
        return -1

def Type(avance):
    return avance + 1

def Stmt(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'LLAVE_APERTURA':
        avance = avance + 1
        terminal = token[avance].getNombreToken()
        if terminal == 'LLAVE_CERRADURA': 
            return avance + 1
        else:
            return -1
    else:
        return -1

# varnames
def DecList(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID':
        avance = Varnames(avance, token)
        return avance
    else:
        return avance

def Varnames(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID':
        avance = avance + 1
        terminal = token[avance].getNombreToken()

        if terminal == 'CORCHETE_APERTURA':
            avance = avance + 1
            avance = ArrayDecl(avance, token)
            if avance == -1:
                return avance

        elif terminal == 'ATR':
            avance = avance + 1
            avance = VarDecInit(avance,token)
            if avance == -1:
                return avance

        elif terminal == 'COMA':
            avance = avance + 1
            avance = DecList(avance, token)
            if avance == -1:
                return avance
            return avance    
        
        terminal = token[avance].getNombreToken()
        if terminal == 'PUNTOCOMA':
            return avance + 1
        else:
            return -1
    else:
        return -1        

def VarDecList(avance, token):
    avance = Type(avance)
    avance = Varnames(avance, token)
    return avance

def VarsDecList(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR':
        avance = VarDecList(avance, token)
        return VarsDecList(avance, token)
    else:
        return avance

def Vars(avance, token):
    terminal = token[avance].getNombreToken()
    
    if terminal == 'CORCHETE_APERTURA':
        avance = avance + 1
        avance = ArrayDecl(avance, token)
        if avance == -1:
            return avance

    elif terminal == 'ATR':
        avance = avance + 1
        avance = VarDecInit(avance,token)
        if avance == -1:
            return avance

    elif terminal == 'COMA':
        avance = avance + 1
        avance = DecList(avance, token)
        return avance
    
    terminal = token[avance].getNombreToken()
    if terminal == 'PUNTOCOMA':
        return avance + 1
    else:
        return -1

def Param(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR':
        avance = avance + 1 
        terminal = token[avance].getNombreToken()
        if terminal == 'ID':
            return avance + 1
        else:
            return -1
    else:
        return -1
def ParamsPrima(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'COMA':
        avance = avance + 1
        avance = Param(avance, token)
        if avance == -1:
            return avance
        terminal = token[avance].getNombreToken()
        if terminal == 'COMA':
            avance = ParamsPrima(avance, token)
        else:
            return avance 
    else:
        return avance

def Params(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR':
        avance = Param(avance, token)
        if avance == -1:
            return avance
        terminal = token[avance].getNombreToken()
        if terminal == 'COMA':
            avance = ParamsPrima(avance, token)
            return avance
        else:
            return avance
    else:
        return avance

def FuncName(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID' or terminal == 'MAIN':
        avance = avance + 1
        terminal = token[avance].getNombreToken()
        if terminal == 'PARENTESIS_APERTURA':
            avance = avance + 1
            avance = Params(avance, token)
            if avance == -1:
                return avance
            terminal = token[avance].getNombreToken()
            if terminal == 'PARENTESIS_CERRADURA':
                avance = avance + 1
                avance = Stmt(avance, token)
                return avance
            else:
                return -1
        else:
            return -1

def FuncDecList(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR':
        avance = avance + 1
        avance = FuncName(avance, token)
        return avance
    elif terminal == 'VOID':
        avance = avance + 1
        avance = FuncName(avance, token)
        return avance
    else:
        return -1

def FuncDecListPrima(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR' or terminal == 'VOID':
        avance = FuncDecList(avance,token)
        if avance == -1:
            return avance
        terminal = token[avance].getNombreToken()
        if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR' or terminal == 'VOID':
            avance = FuncDecListPrima(avance, token)
            return avance
    else:
        return avance

def FuncsDecList(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR' or terminal == 'VOID':
        avance = FuncDecList(avance, token)
        avance = FuncDecListPrima(avance, token)
        return avance
    else:
        return -1

def Decl(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'CORCHETE_APERTURA' or terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR' or terminal == 'COMA' or terminal == 'ATTR' or terminal == 'PUNTOCOMA':
        avance = Vars(avance, token)
        if avance == -1:
            return avance
        avance = VarsDecList(avance, token)
        if avance == -1:
            return -1
        avance = FuncsDecList(avance, token)
        return avance
    else:
        return -1

def FuncsPrima(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'PARENTESIS_APERTURA':
        avance = avance + 1
        avance = Params(avance, token)
        if avance == -1:
            return -1
        terminal = token[avance].getNombreToken()
        if terminal == 'PARENTESIS_CERRADURA':
            avance = Stmt(avance, token)
            if avance == -1:
                return -1
            avance = FuncDecListPrima(avance, token)
            return avance
    else:
        return -1

def program (avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR':
        avance = Type(avance)
        terminal = token[avance].getNombreToken()
        if terminal != 'ID':
            return -1
        avance = avance + 1
        terminal = token[avance].getNombreToken()
        if terminal == 'CORCHETE_APERTURA' or terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR' or terminal == 'COMA' or terminal == 'ATTR' or terminal == 'PUNTOCOMA':
            return Decl(avance,token)
        else:
            return -1
    elif terminal == 'VOID':
        avance = avance + 1
        terminal = token[avance].getNombreToken()
        if terminal != 'MAIN':
            return -1
        avance = avance + 1
        terminal = token[avance].getNombreToken()
        if terminal == 'PARENTESIS_APERTURA':
            avance = FuncsPrima(avance, token)


def inicial(token):
    avance = 0
    avance = program(avance, token)
    if avance == -1:
        print("Hubo un error de sintaxis")
    else:
        print("El programa es correcto en sintaxis")


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
        inicial(token)
        """token += t
        lexema += lex
        fila += lin
        columna += col
        """
    ##print('\nTokens reconocidos: ', token)

