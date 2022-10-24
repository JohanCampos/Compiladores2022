
def initializate
    #cada estado guarda el estado ligado dependiendo de su transición
    #[digito,-,.,otro,+,E]; el estado 0 es vacío; f es estado de aceptación
    tabla = [[2,1,0,0,0,0],[2,0,0,0,0,0],[2,3,4,3,3,3],["f","f","f","f","f","f"],
    [5,0,0,0,0,0],[5,6,6,6,6,7],["f","f","f","f","f","f"],[9,8,0,0,8,0],
    [9,0,0,0,0,0],[9,10,10,10,10,10],["f","f","f","f","f","f"]]
    return tabla
end

def mover(caracter,posicion,tabla)
    #preguntar si es un dígito
    if Integer === caracter
        elemento = 1
    #preguntar si es un -
    elsif caracter == "-"
        elemento = 2
    #preguntar si es un .
    elsif caracter == "."
        elemento = 3
    #preguntar si es un +
    elsif caracter == "+"
        elemento = 4
    #preguntar si es un E    
    elsif caracter == "E"
        elemento = 5
    #Caso de otro
    else
        elemento = 6
    end
    estadoInicial = tabla[posicion]
    estadoFinal = estadoInicial[elemento]
    if estadoFinal == 0
        return false
    elsif estadoFinal == "f"
        return true
    else
        return estadoFinal
    end
    return estadoFinal        
end

tablaAsignacion = initializate
puts("Ingrese su cadena a analizar. \n")
cadena = gets.chomp
cadena = cadena.upcase
posicion = 0
condicion = false
while condicion == false
    cadena.each do |caracter|
        posicion = mover(caracter,posicion)
        if posicion == false | posicion == true
            break
        end
    end
end
if posicion == false
    puts(cadena + " no es un dígito.")
elsif posicion == true
    puts(cadena + " es un dígito.")
gets.chomp