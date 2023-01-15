class Token:

    nombre_token =""
    valor_token=""
    fila = 0
    columna = 0

    def setNombreToken(self, nombre_token):
        self.nombre_token = nombre_token

    def setValorToken(self, valor_token):
        self.valor_token = valor_token

    def setFila(self, fila):
        self.fila = fila

    def setColumna(self, columna):
        self.columna = columna

    def setAtributos(self, nombre_token, valor_token, fila, columna):
        self.setNombreToken(nombre_token)
        self.setValorToken(valor_token)
        self.setFila(fila)
        self.setColumna(columna)

    def getNombreToken(self):
        return self.nombre_token

    def getValorToken(self):
        return self.valor_token

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna

    def __str__(self):
        print("Token: {"+self.nombre_token+"} - Valor: {"+self.valor_token+"} - Fila: {"+str(self.fila)+"} - Columna: {"+str(self.columna)+"}")