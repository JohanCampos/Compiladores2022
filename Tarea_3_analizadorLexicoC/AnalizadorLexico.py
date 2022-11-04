import re


class AnalizadorLexico:
    # Fila del Token
    lin_num = 1

    def tokenize(self, code):
        reglas = [
            ('MAIN', r'main'),          # main
            ('INT', r'int'),            # int
            ('FLOAT', r'float'),        # float
            ('IF', r'if'),              # if
            ('ELSE', r'else'),          # else
            ('WHILE', r'while'),        # while
            ('READ', r'read'),          # read
            ('PRINT', r'print'),        # print
            ('PARENTESIS_APERTURA', r'\('),        # (
            ('PARENTESIS_CERRADURA', r'\)'),        # )
            ('LLAVE_APERTURA', r'\{'),          # {
            ('LLAVE_CERRADURA', r'\}'),          # }
            ('COMA', r','),            # ,
            ('PUNTOCOMA', r';'),           # ;
            ('IGUAL', r'=='),              # ==
            ('NOIGUAL', r'!='),              # !=
            ('MAYORIGUAL', r'<='),              # <=
            ('MENORIGUAL', r'>='),              # >=
            ('OR', r'\|\|'),            # ||
            ('AND', r'&&'),             # &&
            ('ATTR', r'\='),            # =
            ('MAYOR', r'<'),               # <
            ('MENOR', r'>'),               # >
            ('MAS', r'\+'),            # +
            ('MENOS', r'-'),            # -
            ('MULT', r'\*'),            # *
            ('DIV', r'\/'),             # /
            ('ID', r'[a-zA-Z]\w*'),     # IDENTIFICADORES
            ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),   # FLOAT
            ('INTEGER_CONST', r'\d(\d)*'),          # INT
            ('NEWLINE', r'\n'),         # SALTO DE LINEA
            ('SKIP', r'[ \t]+'),        # ESPACIO and TABULADOR
            ('MISMATCH', r'.'),         # CUALQUIER OTRO CARACTER
        ]

        #Unimos los tokens para mostrar al final de la ejecución
        tokens_join = '|'.join('(?P<%s>%s)' % x for x in reglas)
        lin_start = 0

        # Lista de la salida del programa
        token = []
        lexema = []
        fila = []
        columna = []

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
                    col = m.start() - lin_start
                    columna.append(col)
                    token.append(token_tipo)
                    lexema.append(token_lexema)
                    fila.append(self.lin_num)
                    # Imprimimos la información del Token
                    print('Token = {0}, Lexema = \'{1}\', Fila = {2}, Columna = {3}'.format(token_tipo, token_lexema, self.lin_num, col))

        return token, lexema, fila, columna
