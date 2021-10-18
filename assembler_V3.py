import re

operations = ['MOV','ADD','SUB','AND','OR','NOT','XOR','SHL','SHR','INC',
            'RST','CMP','JMP','JEQ','JNE','JGT','JLT','JGE','JLE','JCR','JOV',
            'CALL','RET','PUSH','POP']

def text_reader (text_name):
    file = open(text_name)
    lines = file.readlines()
    data = []
    instructions = []
    is_data = False
    is_code = True
    for line in lines:
        if 'DATA:' in line:
            is_data = True
            is_code = False
        elif 'CODE:' in line:
            is_code = True
            is_data = False
        elif is_data == True:
            line = line.split(' ')
            line.pop(0)
            line.pop(0)
            word = line[1]
            word = re.sub('\n', '',word)
            line.pop(1)
            line.append(word)
            data.append(line)
        elif is_code == True:
            line = line.split()
            if len(line) == 2:
                if ',' in line[1]:
                    line[1] = line[1].split(',')
            instructions.append(line)
    return instructions, data

def jump_dic (instructions):
    jumps = {}
    for line in instructions:
        if ':' in line[0]:
            index = instructions.index(line)
            word = line[0]
            word = re.sub(':', '',word)
            jumps[word] = index
            instructions.pop(index)
    return jumps

def hex_to_dec(string):
    if type(string) == str:
        if  "#" in string:
            string = string.replace("#", "")
            return int(string, 16)
        else:
            return int(string)
    return string

def opcodes(operations):
    dic_ins = {}
    cont = 0
    aux = ""
    stringaux = ""
    check = True
    archivo = open("instrucciones.txt")
    for linea in archivo:
        if linea=="\n":
            check = True
            continue

        linea = linea.replace("\n","")

        if linea in operations and check:
            aux = linea
            check = False
            continue

        cont+=1
        if cont==1:
            stringaux=aux+" "+linea

        if cont==2:
            dic_ins[stringaux]=linea
            stringaux=""
            cont = 0
    return dic_ins

def dir_int_changer(instruction):
    if 'J' in instruction[0]:
        instruction.pop(1)
        instruction.insert(1, '(Dir)')
    if type(instruction[1]) is list:
        for i in range(len(instruction[1])):
            if '(B)' == instruction[1][i]:
                pass
            elif '(' in instruction[1][i]:
                instruction[1].pop(i)
                instruction[1].insert(i, '(Dir)')
            elif 'A' != instruction[1][i] and 'B' != instruction[1][i]:
                instruction[1].pop(i)
                instruction[1].insert(i, 'Lit')
    else:
        if '(B)' == instruction[1]:
                pass
        elif '(' in instruction[1] :
            instruction.pop(1)
            instruction.insert(1, '(Dir)')
        elif 'A' != instruction[1] and 'B' != instruction[1]:
            instruction.pop(1)
            instruction.insert(1, 'Lit')
    return instruction

def output_file_writer(new_instrucitons, opc, lit_list):
    file = open('out.out', 'w')
    i = 0
    print('.OUT: ')
    for instruction in new_instrucitons:
        #print(instruction)
        ins_trans = instruction[0]+' '
        if type(instruction[1]) is list :
            arg = ','.join(instruction[1])
        else:
            arg = instruction[1]
        
        ins_trans += arg
        print(str(opc[ins_trans])+str(lit_list[i]))
        file.write(str(opc[ins_trans])+str(lit_list[i]))
        file.write("\n")
        i += 1
    file.close()

def instruction_validator(instruction, len_instructions, opc, operations, jumps):
    
    #print(f'Linea 108: instruction = {instruction}')
    
    # ins_trans & arg
    ins_trans = instruction[0]+' '
    if len(instruction) == 2:
        if type(instruction[1]) is list:
            arg = ','.join(instruction[1])
        elif  "#" in instruction[1]:
            arg = str(instruction[1])
        else: 
            arg = str(instruction[1])

    #RET
    if instruction[0] == 'RET':
        #print(f'Linea 122: Se activa RET')
        if len(instruction) != 1:
            arg = ','.join(instruction[1])
            return f'Instruccion invalida: {ins_trans}{arg} (150)' 
        if len(instruction) == 1:
            return True 
    
    #Non-existent instruction
    if instruction[0] not in operations:
        return f'Instruccion no existe: {ins_trans} {arg}'
    
    #addressing through A
    if type(instruction[1]) is list:
        for argument in instruction[1]:
            if '(A)' in argument:
                return f'No existe direccionamiento a través del registro A: {ins_trans}{arg} (162)'
    else:
        if '(A)' in instruction[1]:
            return f'No existe direccionamiento a través del registro A: {ins_trans}{arg} (165)'
    
    #Number of arguments
    if len(instruction) != 2:
        return f'Instruccion invalida (Cantidad de argumentos): {ins_trans}{arg} (169)'
    if instruction[0] == 'INC':
        if len(instruction[1]) != 1 and '(' not in instruction[1] :
            return f'Instruccion invalida (Cantidad de argumentos): {ins_trans}{arg} (172)'
    if instruction[0] == 'MOV' or instruction[0] == 'CMP':
        if len(instruction[1]) != 2:
            return f'Instruccion invalida (Cantidad de argumentos): {ins_trans}{arg} (1175)'
    if len(instruction[1]) > 2 and type(instruction[1]) is list:
        return f'Instruccion invalida (Cantidad de argumentos): {ins_trans}{arg} (177)'
    if 'J' in instruction:
        if type(instruction[1]) is list:
            return f'Instruccion invalida (Jump con más de un argumento): {ins_trans}{arg} (180)'
    
    #Change Jumps Direction
    if 'J' in instruction[0]:
        instruction = jumps_direction_changer(instruction, jumps)

    # Jumps
    if 'J' in instruction[0]:
        arg = instruction[1]
        try:
            arg = int(arg)
            if arg > len_instructions:
                return f'Direccion fuera de rango: {ins_trans}{instruction[1]} (192)'
        except:
            if '#' in arg:
                arg = hex_to_dec(arg)
                if arg > len_instructions:
                    return f'Direccion fuera de rango: {ins_trans}{instruction[1]} (197)'
            elif 'A' or 'B' in arg:
                return f'No existen saltos con registros: {ins_trans}{arg} (199)'
            else:
                return f'Direccion no valida: {ins_trans}{instruction[1]} (201)'
    
    #Add Literals and dir.
    #print(f'Linea 200: instruction = {instruction}')
    instruction = dir_int_changer(instruction)
    #print(f'Linea 202: instruction cambiada = {instruction}')
    ins_trans = instruction[0]+' '
    if type(instruction[1]) is list:
        arg = ','.join(instruction[1])
    else: 
        arg = str(instruction[1])
    ins_to_chek = ins_trans+arg
    if ins_to_chek in opc.keys():
        return True
    else:
        return f'Instruccion no existe: {ins_to_chek} (216)'

def jumps_direction_changer(instruction, jumps):
    #print(f'Linea 219: instruction = {instruction}')
    try: 
        arg = jumps[instruction[1]]
        instruction.pop(1)
        instruction.append(str(arg))
    except:
        pass
    return instruction

def literal_list_generator (instructions):
    literal_list = []
    for instruction in instructions:
        print(instruction)
        arg = 0
        if type(instruction[1]) is list:
            for arg in instruction[1]:
                if '#' in arg and '(' not in arg:
                    string = arg.replace("#", "")
                    arg = int(string, 16)
                elif '(' in arg and '(B)' not in arg and '#' not in arg:
                    new_arg = ''
                    for letra in arg:
                        if letra != '(' and letra != ')':
                            new_arg = new_arg+letra
                        try:
                            new_arg=int(letra)
                            arg = new_arg
                        except:
                            pass
                
                else:
                    try:
                        arg = int(arg)
                    except:
                        arg = 0
                        pass
                if arg != 0:
                    break
        elif '(' in instruction[1] and '(B)' not in instruction[1] and '#' not in instruction[1]:
            new_arg = ''
            for letra in instruction[1]:
                if letra != '(' and letra != ')':
                    new_arg = new_arg+letra
                try:
                    new_arg=int(letra)
                    arg = new_arg
                except:
                    arg = 0
                    pass   
        else:
            try:
                arg = int(instruction[1]) 
            except:
                arg = 0
                pass
            
        print(arg)
        if int(arg) < 256 and int(arg) >= 0 :
            binary = str(format(arg,'b'))
            while len(binary) < 8:
                binary = '0'+binary
        elif int(arg) < 0 :
            arg = int(arg)+256
            binary = str(format(arg,'b'))
            while len(binary) < 8:
                binary = '0'+binary
        else:
            binary = 'out_of_range'
        
        literal_list.append(binary)  

    return literal_list
'''
def data_direction_changer(instructions, data):
    a = 0
    b  = 0   
    auxiliary_variable = 0
    pc = 0
    while True:
        instruction = instructions[pc]
        if instruction[0] == 'MOV':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = b
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = a
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = instruction[1][1]
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = instruction[1][1]
            #Dir

        elif instruction[0] == 'ADD':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = int(a)+int(b)
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = int(a)+int(b)
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = int(a)+int(instruction[1][1])
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = int(b)+int(instruction[1][1])
        elif instruction[0] == 'ADD':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = b
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = a
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = instruction[1][1]
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = instruction[1][1]
        elif instruction[0] == 'SUB':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = b
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = a
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = instruction[1][1]
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = instruction[1][1]
        elif instruction[0] == 'AND':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = b
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = a
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = instruction[1][1]
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = instruction[1][1]
        elif instruction[0] == 'OR':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = b
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = a
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = instruction[1][1]
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = instruction[1][1]
        elif instruction[0] == 'NOT':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = b
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = a
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = instruction[1][1]
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = instruction[1][1]
        elif instruction[0] == 'XOR':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = b
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = a
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = instruction[1][1]
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = instruction[1][1]
        elif instruction[0] == 'SHL':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = b
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = a
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = instruction[1][1]
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = instruction[1][1]
        elif instruction[0] == 'SHR':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = b
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = a
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = instruction[1][1]
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = instruction[1][1]
        elif instruction[0] == 'INC':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = b
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = a
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = instruction[1][1]
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = instruction[1][1]
        elif instruction[0] == 'RST':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = b
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = a
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = instruction[1][1]
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = instruction[1][1]
        elif instruction[0] == 'CMP':
            #basic
            if instruction[1][0] == 'A' and instruction[1][1] == 'B':
                a = b
            elif instruction[1][0] == 'B' and instruction[1][1] == 'A':
                b = a
            elif instruction[1][0] == 'A' and instruction[1][1] != 'B' and '(' not in instruction[1][1]:
                a = instruction[1][1]
            elif instruction[1][0] == 'B' and instruction[1][1] != 'A' and '(' not in instruction[1][1]:
                b = instruction[1][1]
        elif instruction[0] == 'JMP':
        elif instruction[0] == 'JEQ':
        elif instruction[0] == 'JNE':
        elif instruction[0] == 'JGT':
        elif instruction[0] == 'JLT':
        elif instruction[0] == 'JGE':
        elif instruction[0] == 'JCR':
        elif instruction[0] == 'JOV':
'''    
def data_direction_changer(instructions, data):
    for instruction in instructions:
        #print(instruction)
        direction = False
        if type(instruction[1]) is list:
            for arg in instruction[1]:
                i = instruction[1].index(arg)
                if '(' in arg:
                    direction = True
                arg = re.sub('\(|\)', '', arg)
                
                for dat in data:
                    
                    if dat[0] == arg:
                        if direction == True:
                            new_arg = '('+dat[1]+')'
                            instruction[1].pop(i)
                            instruction[1].insert(i, new_arg)
                        else:
                            new_arg = dat[1]
                            i = instruction[1].index(arg)
                            instruction[1].pop(i)
                            instruction[1].insert(i, new_arg)
        else:
            arg = instruction[1]
            if '(' in arg:
                direction = True
            arg = re.sub('\(|\)', '', arg)
                
            for dat in data:
                    
                if dat[0] == arg:
                    if direction == True:
                        new_arg = '('+dat[1]+')'
                        instruction.pop(1)
                        instruction.insert(1, new_arg)
                    else:
                        new_arg = data[1]
                        i = instruction.index(arg)
                        instruction.pop(1)
                        instruction.insert(1, new_arg)
    return instructions

def main(operations):
    instructions, data = text_reader('p3F_1.ass')
    jumps = jump_dic(instructions)
    opc = opcodes(operations)
    instructions_copy = []
    
    for i in instructions:
        instructions_copy.append(i)
    len_instructions = len(instructions)
    count = 1
    errors = 0
    for instruction in instructions_copy:
        instruction_validation = instruction_validator(instruction, len_instructions, opc, operations, jumps)
        if instruction_validation != True:
            print(f'Error en la linea {count} ->{instruction_validation}')
            errors += 1
        count += 1
    if errors == 0:
        instructions, data = text_reader('p3F_1.ass')
        #print(f'Linea 475: instruction = {instructions}')
        jumps = jump_dic(instructions)
        for instruction in instructions:
            instruction = jumps_direction_changer(instruction, jumps)
        #print(f'Linea 479: instruction = {instructions}')    
        instructions = data_direction_changer(instructions, data)
        #print(f'Linea 481: instruction = {instructions}')
        literal_list = literal_list_generator (instructions)
        for instruction in instructions:
            instruction = dir_int_changer(instruction)
        #print(f'Linea 485: instruction = {instructions}')
        output_file_writer(instructions, opc, literal_list)
        print('Archivo creado con exito!')

main(operations)