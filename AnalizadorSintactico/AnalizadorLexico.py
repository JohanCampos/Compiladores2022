import re
from Token import Token

class AnalizadorLexico:
    # Fila del Token
    lin_num = 1

    def tokenize(self, code):
        reglas = [
            ('MAIN', r'main'),          # main
            ('VOID', r'void'),          # void
            ('INT', r'int'),            # int
            ('BOOLEAN', r'bool'),       # boolean
            ('FLOAT', r'float'),        # float
            ('CHAR', r'char'),          # char
            ('IF', r'if'),              # if
            ('ELSE', r'else'),          # else
            ('WHILE', r'while'),        # while
            ('FOR', r'for'),            # for
            ('STRUCT', r'struct'),      # struct
            ('INCLUDE', r'#include'),   # include
            ('READ', r'read'),          # read
            ('PRINT', r'print'),        # print
            ('RETURN', r'return'),        # return
            ('PARENTESIS_APERTURA', r'\('),        # (
            ('PARENTESIS_CERRADURA', r'\)'),        # )
            ('CORCHETE_APERTURA', r'\['),        # (
            ('CORCHETE_CERRADURA', r'\]'),        # )
            ('LLAVE_APERTURA', r'\{'),          # {
            ('LLAVE_CERRADURA', r'\}'),          # }
            ('COMA', r','),            # ,
            ('PUNTOCOMA', r';'),           # ;
            ('IGUAL', r'=='),              # ==
            ('NOIGUAL', r'!='),              # !=
            ('NEGATION', r'!'),              # !
            ('MAYORIGUAL', r'<='),              # <=
            ('MENORIGUAL', r'>='),              # >=
            ('OR', r'\|\|'),            # ||
            ('AND', r'&&'),             # &&
            ('ATTR', r'\='),            # =
            ('INCLUDE_CONST',r'\<[a-zA-Z]\w*\.[c-h]\>'), #INCLUDE
            ('MAYOR', r'<'),               # <
            ('MENOR', r'>'),               # >
            ('MAS', r'\+'),            # +
            ('MENOS', r'-'),            # -
            ('MULT', r'\*'),            # *
            ('DIV', r'\/'),             # /
            ('ID', r'[a-zA-Z]\w*'),     # IDENTIFICADORES
            ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),   # FLOAT
            ('INTEGER_CONST', r'\d(\d)*'),          # INT
            ('CHAR_CONST', r'\'[a-zA-Z]\''),        #CHAR
            ('TRUE', r'true'),               # TRUE
            ('FALSE', r'false'),          # FALSE
            ('NEWLINE', r'\n'),         # SALTO DE LINEA
            ('SKIP', r'[ \t]+'),        # ESPACIO and TABULADOR
            ('MISMATCH', r'°'),         # CUALQUIER OTRO CARACTER
        ]

        #Unimos los tokens para hacer la busqueda con el renglon del buffer leido
        tokens_join = '|'.join('(?P<%s>%s)' % x for x in reglas)
        lin_start = 0
        tokens = []

        # Analiza la linea para identificar el lexema y su respectivo Token
        for m in re.finditer(tokens_join, code):
            token_tipo = m.lastgroup
            token_lexema = m.group(token_tipo)
            if token_tipo == 'NEWLINE':
                lin_start = m.end()
                self.lin_num += 1
            elif token_tipo == 'SKIP':
                continue
            elif token_tipo == 'MISMATCH':
                raise RuntimeError('%r inesperado en línea %d' % (token_lexema, self.lin_num))
            else:
                    token = Token()
                    col = m.start() - lin_start
                    token.setAtributos(token_tipo,token_lexema,self.lin_num,col)
                    token.__str__()
                    tokens.append(token)
        
        token = Token()
        token.setNombreToken('FIN_PROGRAMA')
        token.__str__()
        tokens.append(token)

        return tokens

        #return token, lexema, fila, columna
