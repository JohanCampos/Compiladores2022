class Buffer:
    def load_buffer(self):
        arq = open('C://Users//Johan//Documents//GitHub//Compiladores2022//AnalizadorSintactico//program.c', 'r')
        text = arq.readline()

        buffer = []
        cont = 1

        while text != "":
            buffer.append(text)
            text = arq.readline()
            cont += 1

            if cont == 10 or text == '':
                # Regresa el buffer completo
                buf = ''.join(buffer)
                cont = 1
                yield buf

                # Reseteamos el buffer
                buffer = []

        arq.close()
