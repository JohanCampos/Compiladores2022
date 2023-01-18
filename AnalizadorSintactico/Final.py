from Buffer import Buffer
from AnalizadorLexico import AnalizadorLexico
from Token import Token

#Notas:----------------------------------------
# Assignement tiene en conjunto primero ID repetido, tanto para id=Assignement como para LogicOr
# Mientras menos saltos de linea y espacios haya en el Archivo C a analizar, mas caracteres lee correctamente(Posible correccion)
# Mientras mas funciones se llaman, mayor informacion se pierde Ejemplo: Funcion ReturnStmt, se tuvo que poner un print porque no hacia la extraccion del token
# En Funs, despues de Params) va FuncStmt, no stmt
# Limite 39
#----------------------------------------------
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

#
def UnaryOp(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'NEGATION':
        avance = coincidir('NEGATION', avance, token)
        return avance
    elif terminal == 'MENOS':
        avance = coincidir('MENOS', avance, token)
        return avance
    else:
        error(1,terminal,['NEGATION','MENOS'])
        return -1


#
def Primary(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID':
        avance = coincidir('ID', avance, token)
        return avance
    #LogicOr
    elif terminal == 'INTEGER_CONST':
        avance = coincidir('INTEGER_CONST', avance, token)
        return avance
    elif terminal == 'FLOAT_CONST':
        avance = coincidir('FLOAT_CONST', avance, token)
        return avance
    elif terminal == 'CHAR_CONST':
        avance = coincidir('CHAR_CONST', avance, token)
        return avance
    elif terminal == 'TRUE':
        avance = coincidir('TRUE', avance, token)
        return avance
    elif terminal == 'FALSE':
        avance = coincidir('FALSE', avance, token)
        return avance
    elif terminal == 'PARENTESIS_APERTURA':
        avance = coincidir('PARENTESIS_APERTURA', avance, token)
        avance = Expresion(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)
        return avance
    else:
        error(1,terminal,['PUNTOCOMA','ID','INTEGER_CONST','FLOAT_CONST','CHAR_CONST','TRUE','FALSE','PARENTESIS_APERTURA'])
        return -1

#
def CallFunc(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'PARENTESIS_APERTURA':
        avance = coincidir('PARENTESIS_APERTURA', avance, token)
        avance = Params(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)

    return avance

#
def Call(avance,token):
    avance = Primary(avance,token)
    if avance == -1:
        return avance
    avance = CallFunc(avance,token)
    return avance

#
def Unary(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID':
        avance = Call(avance,token)
        return avance
    #LogicOr
    elif terminal == 'INTEGER_CONST':
        avance = Call(avance,token)
        return avance
    elif terminal == 'FLOAT_CONST':
        avance = Call(avance,token)
        return avance
    elif terminal == 'CHAR_CONST':
        avance = Call(avance,token)
        return avance
    elif terminal == 'TRUE':
        avance = Call(avance,token)
        return avance
    elif terminal == 'FALSE':
        avance = Call(avance,token)
        return avance
    elif terminal == 'PARENTESIS_APERTURA':
        avance = Call(avance,token)
        return avance
    elif terminal == 'NEGATION':
        avance = UnaryOp(avance, token) 
        if avance == -1:
            return avance
        avance = Unary(avance,token)
        return avance
    elif terminal == 'MENOS':
        avance = UnaryOp(avance, token) 
        if avance == -1:
            return avance
        avance = Unary(avance,token)
        return avance
    else:
        error(1,terminal,['PUNTOCOMA','ID','INTEGER_CONST','FLOAT_CONST','CHAR_CONST','TRUE','FALSE','PARENTESIS_APERTURA','NEGATION','MENOS'])
        return -1

#
def FactorPrima(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'DIV':
        avance = coincidir('DIV',avance,token)
        avance = Unary(avance,token)
        if avance == -1:
            return avance
        avance = FactorPrima(avance,token)
    elif terminal == 'MULT':
        avance = coincidir('MULT',avance,token)
        avance = Unary(avance,token)
        if avance == -1:
            return avance
        avance = FactorPrima(avance,token)

    return avance

#
def Factor(avance,token):
    avance = Unary(avance,token)
    if avance == -1:
        return avance
    avance = FactorPrima(avance,token)
    return avance

#
def TermPrima(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'MENOS':
        avance = coincidir('MENOS',avance,token)
        avance = Factor(avance,token)
        if avance == -1:
            return avance
        avance = TermPrima(avance,token)
    elif terminal == 'MAS':
        avance = coincidir('MAS')
        avance = Factor(avance,token)
        if avance == -1:
            return avance
        avance = TermPrima(avance,token)

    return avance
    
#
def Term(avance,token):
    avance = Factor(avance,token)
    if avance == -1:
        return avance
    avance = TermPrima(avance,token)
    return avance

def LogicOperator(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'MAYOR':
        avance = coincidir('MAYOR',avance,token)
    elif terminal == 'MENOR':
        avance = coincidir('MENOR',avance,token)
    elif terminal == 'MENORIGUAL':
        avance = coincidir('MENORIGUAL',avance,token)
    elif terminal == 'MAYORIGUAL':
        avance = coincidir('MAYORIGUAL',avance,token)
    return avance

#
def ComparisonPrima(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'MAYOR':
        avance = LogicOperator(avance,token)
        avance = Term(avance,token)
        if avance == -1:
            return avance
        avance = ComparisonPrima(avance,token)
    elif terminal == 'MENOR':
        avance = LogicOperator(avance,token)
        avance = Term(avance,token)
        if avance == -1:
            return avance
        avance = ComparisonPrima(avance,token)
    elif terminal == 'MENORIGUAL':
        avance = LogicOperator(avance,token)
        avance = Term(avance,token)
        if avance == -1:
            return avance
        avance = ComparisonPrima(avance,token)
    elif terminal == 'MAYORIGUAL':
        avance = LogicOperator(avance,token)
        avance = Term(avance,token)
        if avance == -1:
            return avance
        avance = ComparisonPrima(avance,token)

    return avance

#
def Comparison(avance,token):
    avance = Term(avance,token)
    if avance == -1:
        return avance
    avance = ComparisonPrima(avance,token)
    return avance

#
def CompOper(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'NOIGUAL':
        avance = coincidir('NOIGUAL',avance,token)
    elif terminal == 'IGUAL':
        avance = coincidir('IGUAL',avance,token)
    return avance

#  
def EqualityPrima(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'NOIGUAL':
        avance = CompOper(avance,token)
        avance = Comparison(avance,token)
        if avance == -1:
            return avance
        avance = EqualityPrima(avance,token)
    elif terminal == 'IGUAL':
        avance = CompOper(avance,token)
        avance = Comparison(avance,token)
        if avance == -1:
            return avance
        avance = EqualityPrima(avance,token)
    return avance

#
def Equality(avance,token):
    avance = Comparison(avance,token)
    if avance == -1:
        return avance
    avance = EqualityPrima(avance,token)
    return avance

#
def LogicAndPrima(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'AND':
        avance = coincidir('AND', avance, token)
        avance = Equality(avance,token)
        if avance == -1:
            return avance
        avance = LogicAndPrima(avance,token)
    return avance

#
def LogicAnd(avance,token):
    avance = Equality(avance,token)
    if avance == -1:
        return avance
    avance = LogicAndPrima(avance,token)
    return avance

#
def LogicOr(avance,token):
    avance = LogicAnd(avance,token)
    if avance == -1:
        return avance
    avance = LogicOrPrima(avance,token)
    return avance
#
def Assigment(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID':
        avance = coincidir('ID', avance, token) 
        avance = coincidir('ATTR', avance, token)  
        if avance == -1:
            return avance
        avance = Assigment(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PUNTOCOMA',avance,token)
        return avance
    #LogicOr
    elif terminal == 'INTEGER_CONST':
        avance = LogicOr(avance,token)
        return avance
    elif terminal == 'FLOAT_CONST':
        avance = LogicOr(avance,token)
        return avance
    elif terminal == 'CHAR_CONST':
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
        error(1,terminal,['PUNTOCOMA','ID','INTEGER_CONST','FLOAT_CONST','CHAR_CONST','TRUE','FALSE','PARENTESIS_APERTURA','NEGATION','MENOS'])
        return -1

#
def Expresion(avance,token):
    avance = Assigment(avance,token)
    return avance
#
def ExprStmt(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID':
        avance = Expresion(avance,token)
        #avance = coincidir('PUNTOCOMA', avance, token)  
        return avance
    elif terminal == 'INTEGER_CONST':
        avance = Expresion(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PUNTOCOMA', avance, token)  
        return avance
    elif terminal == 'FLOAT_CONST':
        avance = Expresion(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PUNTOCOMA', avance, token)  
        return avance
    elif terminal == 'CHAR_CONST':
        avance = Expresion(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PUNTOCOMA', avance, token)  
        return avance
    elif terminal == 'TRUE':
        avance = Expresion(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PUNTOCOMA', avance, token)  
        return avance
    elif terminal == 'FALSE':
        avance = Expresion(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PUNTOCOMA', avance, token)  
        return avance
    elif terminal == 'PARENTESIS_APERTURA':
        avance = Expresion(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PUNTOCOMA', avance, token) 
        return avance 
    else:
        error(1,terminal,['PUNTOCOMA','ID','INTEGER_CONST','FLOAT_CONST','CHAR_CONST','TRUE','FALSE','PARENTESIS_APERTURA'])
        return -1
    

#
def ParamsPrima(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'COMA':
        avance = coincidir('COMA',avance,token)
        avance = Param(avance,token)
        if avance == -1:
            return avance
        avance = ParamsPrima(avance,token)
        return avance
    else:
        return avance

#
def Param(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = TypeSpec(avance, token)
        if avance == -1:
            return avance
        avance = ParamsPrima(avance, token)
        return avance
    elif terminal == 'FLOAT':
        avance = TypeSpec(avance, token)
        if avance == -1:
            return avance
        avance = ParamsPrima(avance, token)
        return avance
    elif terminal == 'CHAR':
        avance = TypeSpec(avance, token)
        if avance == -1:
            return avance
        avance = ParamsPrima(avance, token)
        return avance
    else:
        error(1,terminal,['INT','FLOAT','CHAR'])
        return -1

#
def Params(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = Param(avance, token)
        if avance == -1:
            return avance
        avance = ParamsPrima(avance, token)
        return avance
    elif terminal == 'FLOAT':
        avance = Param(avance, token)
        if avance == -1:
            return avance
        avance = ParamsPrima(avance, token)
        return avance
    elif terminal == 'CHAR':
        avance = Param(avance, token)
        if avance == -1:
            return avance
        avance = ParamsPrima(avance, token)
        return avance
    else:
        return avance
    
#
def FuncDecList(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = TypeSpec(avance, token)
        if avance == -1:
            return avance
        avance = coincidir('PARENTESIS_APERTURA',avance,token)
        if avance == -1:
            return avance
        avance = Params(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)
        if avance == -1:
            return avance
        avance = FuncStmt(avance,token)
        return avance
    elif terminal == 'FLOAT':
        avance = TypeSpec(avance, token)
        if avance == -1:
            return avance
        avance = coincidir('PARENTESIS_APERTURA',avance,token)
        if avance == -1:
            return avance
        avance = Params(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)
        if avance == -1:
            return avance
        avance = FuncStmt(avance,token)
        return avance
    elif terminal == 'CHAR':
        avance = TypeSpec(avance, token)
        if avance == -1:
            return avance
        avance = coincidir('PARENTESIS_APERTURA',avance,token)
        if avance == -1:
            return avance
        avance = Params(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)
        if avance == -1:
            return avance
        avance = FuncStmt(avance,token)
        return avance
    elif terminal == 'VOID':
        avance = coincidir('VOID', avance, token)
        avance = coincidir('ID', avance, token)
        if avance == -1:
            return avance
        avance = coincidir('PARENTESIS_APERTURA',avance,token)
        if avance == -1:
            return avance
        avance = Params(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)
        if avance == -1:
            return avance
        avance = FuncStmt(avance,token)
        return avance
    else:
        error(1,terminal,['INT','FLOAT','CHAR','VOID'])
        return -1


#
def FuncDecListPrima(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = FuncDecList(avance,token)
        if avance == -1:
            return avance
        avance = FuncDecListPrima(avance,token)
        return avance
    elif terminal == 'FLOAT':
        avance = FuncDecList(avance,token)
        if avance == -1:
            return avance
        avance = FuncDecListPrima(avance,token)
        return avance
    elif terminal == 'CHAR':
        avance = FuncDecList(avance,token)
        if avance == -1:
            return avance
        avance = FuncDecListPrima(avance,token)
        return avance
    elif terminal == 'VOID':
        avance = FuncDecList(avance,token)
        if avance == -1:
            return avance
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
    elif terminal == 'FLOAT_CONST':
        avance = Expresion(avance,token)
        return avance
    elif terminal == 'CHAR_CONST':
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
    if avance == -1:
        return avance
    avance = ForExpr(avance,token)
    if avance == -1:
        return avance
    avance = coincidir('PUNTOCOMA', avance, token)    
    if avance == -1:
        return avance
    avance = ForExpr(avance,token)
    if avance == -1:
        return avance
    avance = coincidir('PUNTOCOMA', avance, token)    
    if avance == -1:
        return avance
    avance = ForExpr(avance,token)  
    if avance == -1:
        return avance
    avance = coincidir('PARENTESIS_CERRADURA',avance,token)
    if avance == -1:
        return avance
    avance = coincidir('LLAVE_APERTURA',avance,token)
    if avance == -1:
        return avance
    avance = Stmts(avance,token)
    if avance == -1:
        return avance
    avance = coincidir('LLAVE_CERRADURA',avance,token)
    return avance

#
def WhileStmt(avance,token):
    avance = coincidir('WHILE',avance,token)
    avance = coincidir('PARENTESIS_APERTURA',avance,token)
    if avance == -1:
        return avance
    avance = Expresion(avance,token)
    if avance == -1:
        return avance
    avance = coincidir('PARENTESIS_CERRADURA',avance,token)
    if avance == -1:
        return avance
    avance = coincidir('LLAVE_APERTURA',avance,token)
    if avance == -1:
        return avance
    avance = Stmts(avance,token)
    if avance == -1:
        return avance
    avance = coincidir('LLAVE_CERRADURA',avance,token)
    return avance

#
def ElseStmt(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ELSE':
        avance = coincidir('ELSE',avance,token)
        avance = coincidir('LLAVE_APERTURA',avance,token)
        if avance == -1:
            return avance
        avance = Stmts(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('LLAVE_CERRADURA',avance,token)
    return avance
#
def IfStmt(avance,token):
    print('enter')
    avance = coincidir('IF',avance,token)
    avance = coincidir('PARENTESIS_APERTURA',avance,token)
    if avance == -1:
        return avance
    avance = Expresion(avance,token)
    if avance == -1:
        return avance
    avance = coincidir('PARENTESIS_CERRADURA',avance,token)
    if avance == -1:
        return avance
    avance = coincidir('LLAVE_APERTURA',avance,token)
    if avance == -1:
        return avance
    avance = Stmts(avance,token)
    if avance == -1:
        return avance
    avance = coincidir('LLAVE_CERRADURA',avance,token)
    if avance == -1:
        return avance
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
        return -1

#
def Stmts(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'ID':
        avance = Stmt(avance,token)
        if avance == -1:
            return avance
        avance = Stmts(avance,token)
        return avance
    elif terminal == 'IF':
        avance = Stmt(avance,token)
        if avance == -1:
            return avance
        avance = Stmts(avance,token)
        return avance
    elif terminal == 'WHILE':
        avance = Stmt(avance,token)
        if avance == -1:
            return avance
        avance = Stmts(avance,token)
        return avance
    elif terminal == 'FOR':
        avance = Stmt(avance,token)
        if avance == -1:
            return avance
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
        if avance == -1:
            return avance
        avance = ReturnStmt(avance,token)
        if avance == -1:
            return avance
        avance = coincidir('LLAVE_CERRADURA', avance, token)
        return avance
    else:
        error(1,terminal,'LLAVE_APERTURA')
        return -1

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
            if avance == -1:
                return avance
            avance = coincidir('PUNTOCOMA', avance, token)  
            return avance
        elif terminal == 'INTEGER_CONST':
            avance = Expresion(avance,token)
            if avance == -1:
                return avance
            avance = coincidir('PUNTOCOMA', avance, token)  
            return avance
        elif terminal == 'FLOAT_CONST':
            avance = Expresion(avance,token)
            if avance == -1:
                return avance
            avance = coincidir('PUNTOCOMA', avance, token)  
            return avance
        elif terminal == 'CHAR_CONST':
            avance = Expresion(avance,token)
            if avance == -1:
                return avance
            avance = coincidir('PUNTOCOMA', avance, token)  
            return avance
        elif terminal == 'TRUE':
            avance = Expresion(avance,token)
            if avance == -1:
                return avance
            avance = coincidir('PUNTOCOMA', avance, token)  
            return avance
        elif terminal == 'FALSE':
            avance = Expresion(avance,token)
            if avance == -1:
                return avance
            avance = coincidir('PUNTOCOMA', avance, token)  
            return avance
        elif terminal == 'PARENTESIS_APERTURA':
            avance = Expresion(avance,token)
            if avance == -1:
                return avance
            avance = coincidir('PUNTOCOMA', avance, token) 
            return avance 
        else:
            error(1,terminal,['PUNTOCOMA','ID','INTEGER_CONST','FLOAT_CONST','CHAR_CONST','TRUE','FALSE','PARENTESIS_APERTURA'])
            return -1
    else:
        return avance


#
def Funcs(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'PARENTESIS_APERTURA':
        avance = coincidir('PARENTESIS_APERTURA', avance, token)
        avance = Params(avance, token)
        if avance == -1:
            return avance
        avance = coincidir('PARENTESIS_CERRADURA',avance,token)
        if avance == -1:
            return avance
        avance = FuncStmt(avance, token)
        if avance == -1:
            return avance
        avance = FuncDecListPrima(avance,token)
        return avance
    else:
        error(1,terminal,'PARENTESIS_APERTURA')

#
def Decl2(avance,token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = TypeSpec(avance, token)
        if avance == -1:
            return avance
        avance = Decl(avance, token)
        return avance
    elif terminal == 'FLOAT':
        avance = TypeSpec(avance, token)
        if avance == -1:
            return avance
        avance = Decl(avance, token)
        return avance
    elif terminal == 'CHAR':
        avance = TypeSpec(avance, token)
        if avance == -1:
            return avance
        avance = Decl(avance, token)
        return avance
    elif terminal == 'VOID':
        avance = coincidir('VOID', avance, token)
        avance = coincidir('ID', avance, token)
        if avance == -1:
            return avance
        avance = Funcs(avance,token)
        return avance
    else:
        error(1,terminal,['INT','FLOAT','CHAR','VOID'])
        return -1

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
        return -1


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
    if avance == -1:
        return avance
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

    if avance == -1:
        return avance
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
        return -1
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
    elif terminal == 'PUNTOCOMA':
        avance == Vars(avance,token)
        return avance
    else:
        error(1,terminal,['PARENTESIS_APERTURA','CORCHETE_APERTURA','ATTR','COMA','PUNTOCOMA'])
        return -1

#
def program(avance, token):
    terminal = token[avance].getNombreToken()
    if terminal == 'INT':
        avance = TypeSpec(avance, token)
        if avance == -1:
            return avance
        avance = Decl(avance, token)
        return avance
    elif terminal == 'FLOAT':
        avance = TypeSpec(avance, token)
        if avance == -1:
            return avance
        avance = Decl(avance, token)
        return avance
    elif terminal == 'CHAR':
        avance = TypeSpec(avance, token)
        if avance == -1:
            return avance
        avance = Decl(avance, token)
        return avance
    elif terminal == 'VOID':
        avance = coincidir('VOID', avance, token)
        avance = coincidir('ID', avance, token)
        if avance == -1:
            return avance
        avance = Funcs(avance,token)
        return avance
    else:
        error(1,terminal,['INT','FLOAT','CHAR','VOID'])
        return -1

if __name__ == '__main__':
    Buffer = Buffer()
    Analizador = AnalizadorLexico()
    tokens = Token()
    

    # Lista de cada lista devuelta por la función tokenize
    #token = []
    #lexema = []
    #fila = []
    #columna = []

    # Obtenemos los tokens y recargams el buffer
    for i in Buffer.load_buffer():
        tokens = Analizador.tokenize(i)
        """token += t
        lexema += lex
        fila += lin
        columna += col
        """
    
        
    token = Token()
    token.setNombreToken('FIN_PROGRAMA')
    token.__str__()
    tokens.append(token)

    avance = 0
    avance = program(avance, tokens)
    if avance != -1:
        print('La sintaxis es correcta')
    ##print('\nTokens reconocidos: ', token)

