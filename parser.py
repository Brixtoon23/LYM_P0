variables = []
functions = {}

def parse_new_var(tokens):
    
    if tokens[1] == "=" and tokens[2] == "VALUE" and tokens[3] == ";":
        variables.append(tokens[0])
        return True
    else:
        return False
    
def parse_assign(tokens):
    
    if tokens[0] in variables and tokens[1] == "=" and tokens[2] == "VALUE" and tokens[3] == ";":
        return True
    else:
        return False

def parse_nFunctions(tokens):

    n_functions = ["turnToMy", "walk", "jump", "drop", "pick", "grab", "letGo", "pop"]
    if tokens[0] in n_functions and tokens[2] == ";":
        inside = tokens[1]
        if inside[0] == "VALUE" or inside[0] in variables:
            return True
    return False

def parse_turnToMy(tokens):
    
    if tokens[0] == "turnToMy" and tokens[2] == ";":
        inside = tokens[1]
        if inside[0] == "RL" or "B":
            return True
    return False

def parse_turnToThe(tokens):
    
    if tokens[0] == "turnToThe" and tokens[2] == ";":
        inside = tokens[1]
        if inside[0] == "O":
            return True
    return False

def parse_moves(tokens):

    if tokens[0] == "moves" and tokens[2] == ";":
        inside = tokens[1]
        check = True
        for i in range(0, len(inside)):
            if i % 2 == 0:
                if inside[i] != "RL" and inside[i] != "FB":
                    check = False
            else:
                if inside[i] != ",":
                    check = False
        
        if check:
                return True
    return False

def parse_nop(tokens):
    if tokens[0] == "nop" and tokens[1] == ";":
        return True
    return False

def parse_safeExe(tokens):

    f5_11_redirect = {
        "walk": parse_nFunctions,
        "jump": parse_nFunctions,
        "drop": parse_nFunctions,
        "pick": parse_nFunctions,
        "grab": parse_nFunctions,
        "letGo": parse_nFunctions,
        "pop": parse_nFunctions,
    }

    if tokens[0] in f5_11_redirect:
        return f5_11_redirect[tokens[0]](tokens)
    else:
        return False 

def parse_block(tokens):
    
    i = 0

    redirect_function = {
        "turnToMy": parse_turnToMy,
        "turnToThe": parse_turnToThe,
        "walk": parse_nFunctions,
        "jump": parse_nFunctions,
        "drop": parse_nFunctions,
        "pick": parse_nFunctions,
        "grab": parse_nFunctions,
        "letGo": parse_nFunctions,
        "pop": parse_nFunctions,
        "moves": parse_moves,
        "nop": parse_nop,
        "safeExe": parse_safeExe,
        "if": parse_if,
        "do": parse_do,
        "repeat": parse_repeat,
    }

    sum_to_i = {
        "turnToMy": 3,
        "turnToThe": 3,
        "walk": 3,
        "jump": 3,
        "drop": 3,
        "pick": 3,
        "grab": 3,
        "letGo": 3,
        "pop": 3,
        "moves": 3,
        "nop": 2,
        "safeExe": 3,
        "if": 7,
        "do": 4,
        "repeat": 4,

    }

    while i < len(tokens):
        instruction_name = tokens[i]
        if instruction_name in redirect_function:

            sublist = tokens[i:i+sum_to_i[instruction_name]]
            if not redirect_function[tokens[i]](sublist):
                return False
            i += sum_to_i[instruction_name]
        else:
            return False
    return True

def parse_condition(tokens):
    
    if tokens[0] == "isBlocked?":
        inside = tokens[1]
        if inside[0] == "RL" or "F" or "B":
            return True
    elif tokens[0] == "isFacing?":
        inside = tokens[1]
        if inside[0] == "O":
            return True
    elif tokens[0] == "zero?":
        if tokens[1] == "VALUE" or tokens[1] in variables:
            return True
    elif tokens[0] == "not":
        return parse_condition(tokens[1])
    
    return False
    
def parse_if(tokens):
    if tokens[0] == "if" and tokens[-1] == "fi":
        check_condition = parse_condition(tokens[1:2])
        if check_condition and tokens[3] == "then":
            check_b1 = parse_block(tokens[4])
            if check_b1 and tokens[5] == "else":
                check_b2 = parse_block(tokens[6])
                if check_b2:
                    return True
    return False

def parse_do(tokens):
    if tokens[0] == "do" and tokens[-1] == "od":
        check_condition = parse_condition(tokens[1:2])
        if check_condition:
            check_b = parse_block(tokens[3])
            if check_b:
                return True
    return False

def parse_repeat(tokens):
    if tokens[0] == "repeat" and (tokens[1] == "VALUE" or tokens[1] in variables) and tokens:
       check_b = parse_block(tokens[3])
       if check_b:
            return True
    return False

def parse_control_structure(tokens):

    redirect_function = {
        "if": parse_if,
        "do": parse_do,
        "repeat": parse_repeat,
    }

    if tokens[0] in redirect_function:
        return redirect_function[tokens[0]](tokens)
    else:
        return False



def parse(tokens):
    return parse_block(tokens)