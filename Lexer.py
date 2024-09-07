LPAREN = '(' 
RPAREN = ')'
COMMA = ','
SEMICOLON = ';'

def lexer(input_string):
    tokens = []
    temp_token = ''
    pila = []

    # Diccionario para realizar las sustituciones
    reemplazos = {
        "right": "RL", "left": "RL",
        "back": "B", "forward": "FB", "backwards": "FB",
        "north": "O", "south": "O", "west": "O", "east": "O",
        "size": "VALUE", "myX": "VALUE", "myY": "VALUE",
        "myChips": "VALUE", "myBalloons": "VALUE",
        "balloonsHere": "VALUE", "chipsHere": "VALUE", 
        "roomForChips": "VALUE", "front": "F"
    }

    for char in input_string:
        # TOKENS PARENTESIS - SUBLISTAS
        if char == '(':
            if temp_token:
                temp_token = reemplazos.get(temp_token, temp_token)
                tokens.append(temp_token)
                temp_token = ''
            pila.append(tokens)  # Guardar la lista actual
            tokens = []  # Crear nueva sublista para paréntesis
        elif char == ')':
            if temp_token:
                if temp_token.isdigit():  # Si es número, reemplazar por VALUE
                    tokens.append("VALUE")
                else:
                    temp_token = reemplazos.get(temp_token, temp_token)
                    tokens.append(temp_token)
                temp_token = ''
            if pila:
                sup_token = pila.pop()  # Recuperar la lista anterior
                sup_token.append(tokens)  # Insertar la sublista
                tokens = sup_token  # Volver a la lista superior
            else:
                print('Error con los paréntesis, por favor verificar.')

        # TOKENS LLAVES - SUBLISTAS
        elif char == '{':
            if temp_token:
                if temp_token.isdigit():  # Si es número, reemplazar por VALUE
                    tokens.append("VALUE")
                else:
                    temp_token = reemplazos.get(temp_token, temp_token)
                    tokens.append(temp_token)
                temp_token = ''
            pila.append(tokens)  # Guardar la lista actual
            tokens = []  # Crear nueva sublista para las llaves
        elif char == '}':
            if temp_token:
                if temp_token.isdigit():  # Si es número, reemplazar por VALUE
                    tokens.append("VALUE")
                else:
                    temp_token = reemplazos.get(temp_token, temp_token)
                    tokens.append(temp_token)
                temp_token = ''
            if pila:
                sup_token = pila.pop()  # Recuperar la lista anterior
                sup_token.append(tokens)  # Insertar la sublista
                tokens = sup_token  # Volver a la lista superior
            else:
                print('Error con las llaves, por favor verificar.')

        # COMAS COMO TOKENS SEPARADOS
        elif char == ',':
            if temp_token:
                if temp_token.isdigit():  # Si es número, reemplazar por VALUE
                    tokens.append("VALUE")
                else:
                    temp_token = reemplazos.get(temp_token, temp_token)
                    tokens.append(temp_token)
                temp_token = ''
            tokens.append(COMMA)

        # PUNTOS Y COMAS COMO TOKENS SEPARADOS
        elif char == ';':
            if temp_token:
                if temp_token.isdigit():  # Si es número, reemplazar por VALUE
                    tokens.append("VALUE")
                else:
                    temp_token = reemplazos.get(temp_token, temp_token)
                    tokens.append(temp_token)
                temp_token = ''
            tokens.append(SEMICOLON)

        # PALABRAS Y NUMEROS
        elif char.isspace():
            if temp_token:
                if temp_token.isdigit():  # Si es número, reemplazar por VALUE
                    tokens.append("VALUE")
                else:
                    temp_token = reemplazos.get(temp_token, temp_token)
                    tokens.append(temp_token)
                temp_token = ''
        elif char.isdigit():
            temp_token += char
        else:
            if temp_token.isdigit():  # Si antes había un número, reemplazar por VALUE
                tokens.append("VALUE")
                temp_token = ''
            temp_token += char

    # Añadir cualquier token restante
    if temp_token:
        if temp_token.isdigit():  # Si es número, reemplazar por VALUE
            tokens.append("VALUE")
        else:
            temp_token = reemplazos.get(temp_token, temp_token)
            tokens.append(temp_token)

    if len(pila) > 0:
        print('Error: paréntesis o llaves desbalanceadas.')

    return tokens
