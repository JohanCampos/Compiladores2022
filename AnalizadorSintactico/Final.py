
from Buffer import Buffer
from AnalizadorLexico import AnalizadorLexico
from Token import Token

def error(id, terminal, esperado):
    #tabla Error
    #id = 1: Se esperaba un terminal y recibio uno distinto
    print('Hubo un error en la sintaxis')
    if id == 1:
        print('Recibio un '+terminal+', se esperaba un '+str(esperado)+'.')

#
def coincidir(esperado, avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == esperado:
        return avance + 1 
    else:
        error(1,terminal,esperado)
        return -1

#
def TypeSpec(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = coincidir('INT', avance, token)
        avance = coincidir('ID', avance, token)
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
        return -1


#
def LogicOrPrima(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'OR':
        avance = coincidir('OR', avance, token)
        avance = LogicAnd(avance,token)
    return avance

#----------------CHECKPOINT-------------FALTA FACTOR, TERMPRIMA, FACTOR PRIMA, UNARY, UNARYOP, CALL, CALLFUNC
def Factor(avance,token):
    return avance

def TermPrima(avance,token):
    return avance
    
#
def Term(avance,token):
    avance = Factor(avance,token)
    avance = TermPrima(avance,token)
    return avance

def LogicOperator(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'MAYOR':
        avance == coincidir('MAYOR',avance,token)
    elif terminal == 'MENOR':
        avance == coincidir('MENOR',avance,token)
    elif terminal == 'MENORIGUAL':
        avance == coincidir('MENORIGUAL',avance,token)
    elif terminal == 'MAYORIGUAL':
        avance == coincidir('MAYORIGUAL',avance,token)
    return avance

#
def ComparisonPrima(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'MAYOR':
        avance == LogicOperator(avance,token)
        avance = Term(avance,token)
        avance = ComparisonPrima(avance,token)
    elif terminal == 'MENOR':
        avance == LogicOperator(avance,token)
        avance = Term(avance,token)
        avance = ComparisonPrima(avance,token)
    elif terminal == 'MENORIGUAL':
        avance == LogicOperator(avance,token)
        avance = Term(avance,token)
        avance = ComparisonPrima(avance,token)
    elif terminal == 'MAYORIGUAL':
        avance == LogicOperator(avance,token)
        avance = Term(avance,token)
        avance = ComparisonPrima(avance,token)

    return avance

#
def Comparison(avance,token):
    avance = Term(avance,token)
    avance = ComparisonPrima(avance,token)
    return avance

#
def CompOper(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'NOIGUAL':
        avance == coincidir('NOIGUAL',avance,token)
    elif terminal == 'IGUAL':
        avance == coincidir('IGUAL',avance,token)
    return avance

#  
def EqualityPrima(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'NOIGUAL':
        avance = CompOper(avance,token)
        avance = Comparison(avance,token)
        avance = EqualityPrima(avance,token)
    elif terminal == 'IGUAL':
        avance = CompOper(avance,token)
        avance = Comparison(avance,token)
        avance = EqualityPrima(avance,token)
    return avance

#
def Equality(avance,token):
    avance = Comparison(avance,token)
    avance = EqualityPrima(avance,token)
    return avance

#
def LogicAndPrima(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'AND':
        avance = coincidir('AND', avance, token)
        avance = Equality(avance,token)
        avance = LogicAndPrima(avance,token)
    return avance

#
def LogicAnd(avance,token):
    avance = Equality(avance,token)
    avance = LogicAndPrima(avance,token)
    return avance

#
def LogicOr(avance,token):
    avance = LogicAnd(avance,token)
    avance = LogicOrPrima(avance,token)
    return avance
#
def Assigment(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID':
        avance = coincidir('ID', avance, token) 
        avance = coincidir('ATTR', avance, token)  
        avance = Assigment(avance,token)
        avance = coincidir('PUNTOCOMA',avance,token)
        return avance
    #LogicOr
    elif terminal == 'INTEGER_CONST':
        avance = LogicOr(avance,token)
        return avance
    elif terminal == 'FLOAT_CONTS':
        avance = LogicOr(avance,token)
        return avance
    elif terminal == 'CHAR_CONTS':
        avance = LogicOr(avance,token)
        return avance
    elif terminal == 'TRUE':
        avance = LogicOr(avance,token)
        return avance
    elif terminal == 'FALSE':
        avance = LogicOr(avance,token)
        return avance
    elif terminal == 'PARENTESIS_APERTURA':
        avance = LogicOr(avance,token)
        return avance 
    elif terminal == 'NEGATION':
        avance = LogicOr(avance,token)
        return avance 
    elif terminal == 'MENOS':
        avance = LogicOr(avance,token)
        return avance 
    else:
        error(1,terminal,['PUNTOCOMA','ID','INTEGER_CONST','FLOAT_CONTS','CHAR_CONTS','TRUE','FALSE','PARENTESIS_APERTURA','NEGATION','MENOS'])

#
def Expresion(avance,token):
    avance = Assigment(avance,token)
    return avance
#
def ExprStmt(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID':
        avance = Expresion(avance,token)
        avance = coincidir('PUNTOCOMA', avance, token)  
        return avance
    elif terminal == 'INTEGER_CONST':
        avance = Expresion(avance,token)
        avance = coincidir('PUNTOCOMA', avance, token)  
        return avance
    elif terminal == 'FLOAT_CONTS':
        avance = Expresion(avance,token)
        avance = coincidir('PUNTOCOMA', avance, token)  
        return avance
    elif terminal == 'CHAR_CONTS':
        avance = Expresion(avance,token)
        avance = coincidir('PUNTOCOMA', avance, token)  
        return avance
    elif terminal == 'TRUE':
        avance = Expresion(avance,token)
        avance = coincidir('PUNTOCOMA', avance, token)  
        return avance
    elif terminal == 'FALSE':
        avance = Expresion(avance,token)
        avance = coincidir('PUNTOCOMA', avance, token)  
        return avance
    elif terminal == 'PARENTESIS_APERTURA':
        avance = Expresion(avance,token)
        avance = coincidir('PUNTOCOMA', avance, token) 
        return avance 
    else:
        error(1,terminal,['PUNTOCOMA','ID','INTEGER_CONST','FLOAT_CONTS','CHAR_CONTS','TRUE','FALSE','PARENTESIS_APERTURA'])
    

#
def ParamsPrima(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'COMA':
        avance = coincidir('COMA',avance,terminal)
        avance = Param(avance,terminal)
        avance = ParamsPrima(avance,terminal)
        return avance
    else:
        return avance

#
def Param(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = TypeSpec(avance, token)
        avance = ParamsPrima(avance, token)
        return avance
    elif terminal == 'FLOAT':
        avance = TypeSpec(avance, token)
        avance = ParamsPrima(avance, token)
        return avance
    elif terminal == 'CHAR':
        avance = coincidir(avance, token)
        avance = ParamsPrima(avance, token)
        return avance
    else:
        error(1,terminal,['INT','FLOAT','CHAR'])

#
def Params(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = Param(avance, token)
        avance = ParamsPrima(avance, token)
        return avance
    elif terminal == 'FLOAT':
        avance = Param(avance, token)
        avance = ParamsPrima(avance, token)
        return avance
    elif terminal == 'CHAR':
        avance = Param(avance, token)
        avance = ParamsPrima(avance, token)
        return avance
    else:
        return avance
    
#
def FuncDecList(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = TypeSpec(avance, token)
        avance = coincidir('PARENTESIS_APERTURA',avance,token)
        avance = Params(avance,token)
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)
        avance = FuncStmt(avance,token)
        return avance
    elif terminal == 'FLOAT':
        avance = TypeSpec(avance, token)
        avance = coincidir('PARENTESIS_APERTURA',avance,token)
        avance = Params(avance,token)
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)
        avance = FuncStmt(avance,token)
        return avance
    elif terminal == 'CHAR':
        avance = TypeSpec(avance, token)
        avance = coincidir('PARENTESIS_APERTURA',avance,token)
        avance = Params(avance,token)
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)
        avance = FuncStmt(avance,token)
        return avance
    elif terminal == 'VOID':
        avance = coincidir('VOID', avance, token)
        avance = coincidir('ID', avance, token)
        avance = coincidir('PARENTESIS_APERTURA',avance,token)
        avance = Params(avance,token)
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)
        avance = FuncStmt(avance,token)
        return avance
    else:
        error(1,terminal,['INT','FLOAT','CHAR','VOID'])


#
def FuncDecListPrima(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = FuncDecList(avance,token)
        avance = FuncDecListPrima(avance,token)
        return avance
    elif terminal == 'FLOAT':
        avance = FuncDecList(avance,token)
        avance = FuncDecListPrima(avance,token)
        return avance
    elif terminal == 'CHAR':
        avance = FuncDecList(avance,token)
        avance = FuncDecListPrima(avance,token)
        return avance
    elif terminal == 'VOID':
        avance = FuncDecList(avance,token)
        avance = FuncDecListPrima(avance,token)
        return avance
    else:
        return avance

#
def ForExpr(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID':
        avance = Expresion(avance,token)
        return avance
    elif terminal == 'INTEGER_CONST':
        avance = Expresion(avance,token)
        return avance
    elif terminal == 'FLOAT_CONTS':
        avance = Expresion(avance,token)
        return avance
    elif terminal == 'CHAR_CONTS':
        avance = Expresion(avance,token)
        return avance
    elif terminal == 'TRUE':
        avance = Expresion(avance,token)
        return avance
    elif terminal == 'FALSE':
        avance = Expresion(avance,token)
        return avance
    elif terminal == 'PARENTESIS_APERTURA':
        avance = Expresion(avance,token)
        return avance 
    elif terminal == 'NEGATION':
        avance = Expresion(avance,token)
        return avance 
    elif terminal == 'MENOS':
        avance = Expresion(avance,token)
        return avance 
    else:
        return avance 

#
def ForStmt(avance,token):
    avance = coincidir('FOR',avance,token)
    avance = coincidir('PARENTESIS_APERTURA',avance,token)
    avance = ForExpr(avance,token)
    avance = coincidir('PUNTOCOMA', avance, token)    
    avance = ForExpr(avance,token)
    avance = coincidir('PUNTOCOMA', avance, token)    
    avance = ForExpr(avance,token)  
    avance = coincidir('PARENTESIS_CERRADURA',avance,token)
    avance = coincidir('LLAVE_APERTURA',avance,token)
    avance = Stmts(avance,token)
    avance = coincidir('LLAVE_CERRADURA',avance,token)
    return avance

#
def WhileStmt(avance,token):
    avance = coincidir('WHILE',avance,token)
    avance = coincidir('PARENTESIS_APERTURA',avance,token)
    avance = Expresion(avance,token)
    avance = coincidir('PARENTESIS_CERRADURA',avance,token)
    avance = coincidir('LLAVE_APERTURA',avance,token)
    avance = Stmts(avance,token)
    avance = coincidir('LLAVE_CERRADURA',avance,token)
    return avance

#
def ElseStmt(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ELSE':
        avance = coincidir('ELSE',avance,token)
        avance = coincidir('LLAVE_APERTURA',avance,token)
        avance = Stmts(avance,token)
        avance = coincidir('LLAVE_CERRADURA',avance,token)
    return avance
#
def IfStmt(avance,token):
    avance = coincidir('IF',avance,token)
    avance = coincidir('PARENTESIS_APERTURA',avance,token)
    avance = Expresion(avance,token)
    avance = coincidir('PARENTESIS_CERRADURA',avance,token)
    avance = coincidir('LLAVE_APERTURA',avance,token)
    avance = Stmts(avance,token)
    avance = coincidir('LLAVE_CERRADURA',avance,token)
    avance = ElseStmt(avance,token)
    return avance

#
def Stmt(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID':
        avance = ExprStmt(avance,token)
        return avance
    elif terminal == 'IF':
        avance = IfStmt(avance,token)
        return avance
    elif terminal == 'WHILE':
        avance = WhileStmt(avance,token)
        return avance
    elif terminal == 'FOR':
        avance = ForStmt(avance,token)
        return avance
    else:
        error(1,terminal,['ID','IF','WHILE','FOR'])

#
def Stmts(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID':
        avance = Stmt(avance,token)
        avance = Stmts(avance,token)
        return avance
    elif terminal == 'IF':
        avance = Stmt(avance,token)
        avance = Stmts(avance,token)
        return avance
    elif terminal == 'WHILE':
        avance = Stmt(avance,token)
        avance = Stmts(avance,token)
        return avance
    elif terminal == 'FOR':
        avance = Stmt(avance,token)
        avance = Stmts(avance,token)
        return avance
    else:
        return avance

#
def FuncStmt(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'LLAVE_APERTURA':
        avance = coincidir('LLAVE_APERTURA', avance, token)
        avance = Stmts(avance, token)
        avance = ReturnStmt(avance,token)
        avance = coincidir('LLAVE_CERRADURA', avance, token)
        return avance
    else:
        error(1,terminal,'LLAVE_APERTURA')

#
def ReturnStmt(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'RETURN':
        avance = coincidir('RETURN', avance, token)
        if terminal == 'PUNTOCOMA':
            avance = coincidir('PUNTOCOMA', avance, token)    
            return avance      
        elif terminal == 'ID':
            avance = Expresion(avance,token)
            avance = coincidir('PUNTOCOMA', avance, token)  
            return avance
        elif terminal == 'INTEGER_CONST':
            avance = Expresion(avance,token)
            avance = coincidir('PUNTOCOMA', avance, token)  
            return avance
        elif terminal == 'FLOAT_CONTS':
            avance = Expresion(avance,token)
            avance = coincidir('PUNTOCOMA', avance, token)  
            return avance
        elif terminal == 'CHAR_CONTS':
            avance = Expresion(avance,token)
            avance = coincidir('PUNTOCOMA', avance, token)  
            return avance
        elif terminal == 'TRUE':
            avance = Expresion(avance,token)
            avance = coincidir('PUNTOCOMA', avance, token)  
            return avance
        elif terminal == 'FALSE':
            avance = Expresion(avance,token)
            avance = coincidir('PUNTOCOMA', avance, token)  
            return avance
        elif terminal == 'PARENTESIS_APERTURA':
            avance = Expresion(avance,token)
            avance = coincidir('PUNTOCOMA', avance, token) 
            return avance 
        else:
            error(1,terminal,['PUNTOCOMA','ID','INTEGER_CONST','FLOAT_CONTS','CHAR_CONTS','TRUE','FALSE','PARENTESIS_APERTURA'])
    else:
        return avance


#
def Funcs(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'PARENTESIS_APERTURA':
        avance = coincidir('PARENTESIS_APERTURA', avance, token)
        avance = Params(avance, token)
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)
        avance = FuncStmt(avance, token)
        avance = FuncDecListPrima(avance,token)
        return avance
    else:
        error(1,terminal,'PARENTESIS_APERTURA')

#
def Decl2(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = TypeSpec(avance, token)
        avance = Decl(avance, token)
        return avance
    elif terminal == 'FLOAT':
        avance = TypeSpec(avance, token)
        avance = Decl(avance, token)
        return avance
    elif terminal == 'CHAR':
        avance = TypeSpec(avance, token)
        avance = Decl(avance, token)
        return avance
    elif terminal == 'VOID':
        avance = coincidir('VOID', avance, token)
        avance = coincidir('ID', avance, token)
        avance = Funcs(avance,token)
        return avance
    else:
        error(1,terminal,['INT','FLOAT','CHAR','VOID'])

#
def VarNames(avance,token):
    avance = coincidir('ID',avance,token)
    terminal = token[avance].getNombreToken()
    if terminal == 'CORCHETE_APERTURA':
        avance = ArrayDecl(avance,token)
        return avance
    elif terminal == 'ATTR':
        avance = VarDeclInit(avance,token)
        return avance
    elif terminal == 'COMA':
        avance = DecList(avance,token)
        return avance
    else:
        error(1,terminal,'PARENTESIS_APERTURA')


#
def DecList(avance,token):
    avance = coincidir('COMA',avance,token)
    avance = VarNames(avance, token)
    return avance

#
def VarDeclInit(avance,token):
    avance = coincidir('ATTR',avance,token)
    avance = Expresion(avance,token)
    return avance

#
def ArrayDecl(avance,token):
    avance = coincidir('CORCHETE_APERTURA',avance,token)
    avance = coincidir('INTEGER_CONST',avance,token)
    avance = coincidir('CORCHETE_CERRADURA',avance,token)
    return avance

#
def Vars(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'CORCHETE_APERTURA':
        avance = ArrayDecl(avance,token)
    elif terminal == 'ATTR':
        avance = VarDeclInit(avance,token)
    elif terminal == 'COMA':
        avance = DecList(avance,token)
    else:
        error(1,terminal,'PARENTESIS_APERTURA')

    avance = coincidir('PUNTOCOMA',avance,token)
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = Decl2(avance,token)
        return avance
    elif terminal == 'FLOAT':
        avance = Decl2(avance,token)
        return avance
    elif terminal == 'CHAR':
        avance = Decl2(avance,token)
        return avance
    elif terminal == 'VOID':
        avance = Decl2(avance,token)
        return avance
    else:
        error(1,terminal,['INT','FLOAT','CHAR','VOID'])
#
def Decl(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'PARENTESIS_APERTURA':
        avance = Funcs(avance,token)
        return avance
    elif terminal == 'CORCHETE_APERTURA':
        avance == Vars(avance,token)
        return avance
    elif terminal == 'ATTR':
        avance == Vars(avance,token)
        return avance
    elif terminal == 'COMA':
        avance == Vars(avance,token)
        return avance
    else:
        error(1,terminal,['PARENTESIS_APERTURA','CORCHETE_APERTURA','ATTR','COMA'])

#
def program(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = TypeSpec(avance, token)
        avance = Decl(avance, token)
        return avance
    elif terminal == 'FLOAT':
        avance = TypeSpec(avance, token)
        avance = Decl(avance, token)
        return avance
    elif terminal == 'CHAR':
        avance = TypeSpec(avance, token)
        avance = Decl(avance, token)
        return avance
    elif terminal == 'VOID':
        avance = coincidir('VOID', avance, token)
        avance = coincidir('ID', avance, token)
        avance = Funcs(avance,token)
        return avance
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

