class AnalizadorSintactico:
    
    #Estados: -1 == error

    def inicial(self, token):
        avance = 0
        sintaxis = program(avance, token)
        if avance == -1:
            print("Hubo un error de sintaxis")
        else:
            print("El programa es correcto en sintaxis")
            
    def program (self, avance, token):
        terminal = token[avance].getNombreToken()
        if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR':
            avance = Type(avance)
            terminal = token[avance].getNombreToken()
            if terminal != 'ID':
                return -1
            avance = avance + 1
            terminal = token[avance].getNombreToken()
            if terminal == 'CORCHETE_APERTURA' or terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR' or terminal == 'COMA':
                return Decl(avance,token)
            else:
                return -1
        elif terminal == 'VOID':
            avance = avance + 1
            terminal = token[avance].getNombreToken()
            if terminal != 'ID':
                return -1
            avance = avance + 1
            terminal = token[avance].getNombreToken()
            if terminal == 'PARENTESIS_APERTURA':
                avance = FuncsPrima(avance, token)

    def FuncsPrima(self, avance, token):
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

    def FuncDecListPrima(self, avance, token):
        terminal = token[avance].getNombreToken()
        if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR' or terminal == 'VOID':
            avance = FuncDecList(avance,token)
            if avance == -1:
                return avance
            terminal = token[avance].getNombreToken()
            if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR' or terminal == 'VOID':
                avance = FuncDecListPrime(avance, token)
                return avance
        else:
            return -1

    def Params(self, avance, token):
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
                return -1
        else:
            return -1

    def ParamsPrima(self, avance, token):
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
            return -1

    def Param(self, avance, token):
        terminal = token[avance].getNombreToken()
        if terminal == 'ID':
            return avance + 1
        else:
            return -1

    def Type(self, avance):
        return avance + 1

    def Decl(self, avance, token):
        terminal = token[avance].getNombreToken()
        if terminal == 'CORCHETE_APERTURA' or terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR' or terminal == 'COMA':
            avance = Vars(avance, token)
            if avance == -1:
                return avance
            avance = VarsDecList(avance, token)
            if avance == -1:
                return 
            avance = FuncsDecList(avance, token)
            
            return avance
        else:
            return -1

    def FuncsDecList(self, avance, token):
        terminal = token[avance].getNombreToken()
        if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR':
            avance = FuncDecList(avance, token)
            avance = FuncDecListPrima(avance, token)
            return avance
        else:
            return -1

    def FuncDecList(self, avance, token):
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

    def FuncName(self, avance, token):
        terminal = token[avance].getNombreToken()
        if terminal == 'ID':
            avance = avance + 1
            terminal = token[avance].getNombreToken()
            if terminal == 'PARENTESIS_APERTURA':
                avance = avance + 1
                avance = Params(avance, token)
                if avance == -1:
                    return avance
                terminal = token[avance].getNombreToken()
                if terminal == 'PARENTESIS_CERRADURA':
                    avance = Stmt(avance, token)
                    return avance
                else:
                    return -1

    def Stmt(self, avance, token):
        terminal = token[avance].getNombreToken()
        if terminal == 'PARENTESIS_APERTURA':
            avance = avance + 1
            terminal = token[avance].getNombreToken()
            if terminal == 'PARENTESIS_CERRADURA': 
                avance = avance + 1
                terminal = token[avance].getNombreToken()
                return avance + 1
            else:
                return -1
        else:
            return -1

    def VarsDecList(self, avance, token):
        terminal = token[avance].getNombreToken()
        if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR':
            avance = VarDecList(avance, token)
            VarsDecList(avance, token)
        else:
            return avance

    def VarDecList(self, avance, token):
        avance = Type(avance)
        avance = Varnames(avance, token)
        return avance


    def Vars(self, avance, token):
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

        terminal = token[avance].getNombreToken()
        if terminal == 'PUNTOCOMA':
            return avance + 1
        else:
            return -1
    
    # varnames
    def DecList(self, avance, token):
        terminal = token[avance].getNombreToken()
        
        if terminal == 'INT' or terminal == 'FLOAT' or terminal == 'CHAR':
            avance = avance +1
            avance = Varnames(avance, token)
            return avance
        else:
            return -1

    def Varnames(self, avance, token):
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
            
            terminal = token[avance].getNombreToken()
            if terminal == 'PUNTOCOMA':
                return avance + 1
            else:
                return -1
        else:
            return -1        

    # exp
    def VarDecInit(self, avance, token):
        return avance

    # numero]
    def ArrayDecl(self, avance, token):
        terminal = token[avance].getNombreToken()
        if terminal == 'INTEGER_CONST' or terminal == 'FLOAT_CONST':
            avance = avance + 1
            terminal = token[avance].getNombreToken()
            if terminal == 'CORCHETE_CERRADURA':
                return avance + 1
            else:
                return -1
        else:
            return -1