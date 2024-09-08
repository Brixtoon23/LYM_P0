variables = []
functions = {}
functions_params = {}
ACTUAL_CREATING_FUNCTION = []

def parse_value(value):
    if value == "VALUE" or value in variables:
        return True
    elif len(ACTUAL_CREATING_FUNCTION) > 0:
        for name_function in ACTUAL_CREATING_FUNCTION:
            if value in functions_params[name_function]:
                return True
    return False

def parse_new_var(tokens):
    
    if tokens[1] == "=" and tokens[2] == "VALUE":
        variables.append(tokens[0])
        return True
    else:
        return False
    
def parse_assign(tokens):
    
    if tokens[0] in variables and tokens[1] == "=" and parse_value(tokens[2]) and tokens[3] == ";":
        return True
    else:
        return False

def parse_nFunctions(tokens):

    n_functions = ["turnToMy", "walk", "jump", "drop", "pick", "grab", "letGo", "pop"]
    if tokens[0] in n_functions and tokens[2] == ";":
        inside = tokens[1]
        if parse_value(inside[0]):
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

    inside_function = tokens[1]

    if inside_function[0] in f5_11_redirect:
        inside_function.append(";")
        return f5_11_redirect[inside_function[0]](inside_function)
    else:
        return False 

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
        if parse_value(tokens[1][0]):
            return True
    elif tokens[0] == "not":
        return parse_condition(tokens[1])
    
    return False
    
def parse_if(tokens):
    if tokens[0] == "if" and tokens[-1] == ";" and tokens[-2] == "fi":
        check_condition = parse_condition(tokens[1:3])
        if check_condition and tokens[3] == "then":
            check_b1 = parse_block(tokens[4])
            if check_b1 and tokens[5] == "else":
                check_b2 = parse_block(tokens[6])
                if check_b2:
                    return True
    return False

def parse_do(tokens):
    if tokens[0] == "do" and tokens[-1] == ";" and tokens[-2] == "od":
        check_condition = parse_condition(tokens[1:3])
        if check_condition:
            check_b = parse_block(tokens[3])
            if check_b:
                return True
    return False

def parse_repeat(tokens):
    if tokens[0] == "repeat" and parse_value(tokens[1]) and tokens[2] == "times"  and tokens[-1] == ";" :
       check_b = parse_block(tokens[3])
       if check_b:
            return True
    return False


def parse_exec(tokens):
    if tokens[0] == "EXEC":
        check = parse_block(tokens[1])
        if check:
            return True
    return False

def parse_new(tokens):
    if tokens[0] == "NEW":
        if tokens[1] == "VAR":
            check = parse_new_var(tokens[2:5])
            if check:
                return True
        elif tokens[1] == "MACRO":
            check = parse_new_macro(tokens[2:5])
            if check:
                return True
    return False

def parse_new_macro(tokens):
    ACTUAL_CREATING_FUNCTION.append(tokens[0])
    num_params = 0
    params = tokens[1]
    for i in range(0, len(params)):
        if i % 2 == 0:
            if params[i] == "VALUE":
                ACTUAL_CREATING_FUNCTION.clear()
                return False
            else:
                num_params += 1
                functions_params[tokens[0]] = functions_params.get(tokens[0], [])
                functions_params[tokens[0]].append(params[i])
        else:
            if params[i] != ",":
                ACTUAL_CREATING_FUNCTION.clear()
                return False
    
    functions[tokens[0]] = num_params
    check_b = parse_block(tokens[2])
    if check_b:
        ACTUAL_CREATING_FUNCTION.clear()
        return True
    ACTUAL_CREATING_FUNCTION.clear()
    return False

def parse_function_call(tokens):
    
    inside = tokens[1]
    num_params = 0
    for i in range(0, len(inside)):
        if i % 2 == 0:
            if not parse_value(inside[i]):
                return False
            num_params += 1
        else:
            if inside[i] != ",":
                return False

    if functions[tokens[0]] == num_params and tokens[2] == ";":
        return True
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
        "EXEC": parse_exec,
        "NEW": parse_new,
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
        "if": 9,
        "do": 6,
        "repeat": 5,
        "EXEC": 2,
        "NEW": 5,

    }

    while i < len(tokens):
        instruction_name = tokens[i]
        if instruction_name in redirect_function:

            sublist = tokens[i:i+sum_to_i[instruction_name]]
            if not redirect_function[tokens[i]](sublist):
                return False
            i += sum_to_i[instruction_name]
        
        elif tokens[i] in variables:
            if not parse_assign(tokens[i:i+4]):
                return False
            i += 4
        
        elif tokens[i] in functions:
            sublist = tokens[i:i+3]
            if not parse_function_call(sublist):
                return False
            i += 3
        
        else:
            return False
    return True

def parse(tokens):
    return parse_block(tokens)