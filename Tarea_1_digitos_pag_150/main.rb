
def initializate
    #cada estado guarda el estado ligado dependiendo de su transición
    #[digito,-,.,E,+,otro];
    #Estados de aceptación: 3,5,8,9; estado de aceptación que indica que no es dígito: 9
    tabla = [[3,1,9,9,2,9],[3,9,9,9,9,9],[3,9,9,9,9,9],[3,9,4,9,9,9],[5,9,9,9,9,9],
    [5,9,9,6,9,9],[8,7,9,9,7,9],[8,9,9,9,9,9],[8,9,9,9,9,9],[9,9,9,9,9,9]]
    return tabla
end

def mover(caracter,posicion,tabla)
    #preguntar si es un dígito
    if caracter == "0" || caracter == "1" || caracter == "2" || caracter == "3" || caracter == "4" || caracter == "5" || caracter == "6" || caracter == "7" || caracter =="8" || caracter == "9"
        elemento = 0
    #preguntar si es un -
    elsif caracter == "-"
        elemento = 1
    #preguntar si es un .
    elsif caracter == "."
        elemento = 2
    #preguntar si es un +
    elsif caracter == "+"
        elemento = 4
    #preguntar si es un E    
    elsif caracter == "E"
        elemento = 3
    #Caso de otro
    else
        elemento = 5
    end
    estadoInicial = tabla[posicion]
    estadoFinal = estadoInicial[elemento]
    return estadoFinal        
end

tablaAsignacion = initializate
puts("Ingrese su cadena a analizar. \n")
cadena = gets.chomp
cadenaDividida = cadena.split("")
posicion = 0
for i in (0..(cadenaDividida.length-1))
    posicion = mover(cadenaDividida[i],posicion,tablaAsignacion)
end
if posicion == 9
    puts(cadena + " no es un dígito.")
elsif posicion == 3 || posicion == 5 || posicion == 8
    puts(cadena + " es un dígito.")
else
    puts("La cadena "+ cadena + " está incompleta.")
end 
gets.chomp
