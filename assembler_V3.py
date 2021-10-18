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

def output_file_writer(new_instrucitons, opc, lit_list, file_name):
    out_name = file_name + '.out'
    file = open(out_name, 'w')
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
    out_of_range = False
    literal_out = 'None'
    for instruction in instructions:
        arg = 0
        print('instrucion:', instruction)
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
        elif '#' in instruction[1] and '(' not in instruction[1]:
            arg = instruction[1]
            string = arg.replace("#", "")
            arg = int(string, 16)
        else:
            try:
                arg = int(instruction[1]) 
            except:
                arg = 0
                pass
            
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
            out_of_range = True
            literal_out = instruction
        
        literal_list.append(binary)  

    return literal_list, out_of_range, literal_out

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
                            for a in range(len(data)):
                                if arg in data[a]:
                                    instruction[1].pop(i)
                                    instruction[1].insert(i, '('+str(a)+')')
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
                       for a in range(len(data)):
                            if arg in data[a]:
                                instruction.pop(1)
                                instruction.insert(1, '('+str(a)+')')
                    else:
                        new_arg = data[1]
                        i = instruction.index(arg)
                        instruction.pop(1)
                        instruction.insert(1, new_arg)
    return instructions

def memory_file (data, file_name):
    mem_out = file_name + '.mem'
    file = open(mem_out, 'w')
    for line in data:
        if '#' in line[1]:
            arg = line[1]
            string = arg.replace("#", "")
            arg = int(string, 16)
        try:
            arg = int(line[1])
        except:
            pass

        binary = str(format(arg,'b'))
        while len(binary) < 8:
            binary = '0'+binary
        file.write(binary)
        file.write("\n")

def undeclared_variable_detector (instructions, data):
    for instruction in instructions:
        if type(instruction[1]) is list:
            is_number = 0
            in_data = False
            for arg in instruction[1]:
                try:
                    if '(' in arg:
                        arg = re.sub('\(|\)', '', arg)
                    int(arg)
                    is_number = 1
                except:
                    pass
                if arg != 'A' and arg != 'B' and arg != '(B)' and is_number == 0 and '#' not in arg:
                    if '(' in arg:
                        arg = re.sub('\(|\)', '', arg)
                    for dat in data:
                        if dat[0] == arg:
                            in_data = True
                    if in_data == False:
                        return False, arg
        else:
            arg = instruction[1]
            is_number = 0
            in_data = False
            try:
                if '(' in arg:
                        arg = re.sub('\(|\)', '', arg)
                int(arg)
                is_number = 1
            except:
                pass
            if arg != 'A' and arg != 'B' and arg != '(B)' and is_number == 0 and '#' not in arg:
                if '(' in arg:
                    arg = re.sub('\(|\)', '', arg)
                for dat in data:
                    if dat[0] == arg:
                        in_data = True
                if in_data == False:
                    return False , arg
    return True, 'none'

def main(operations):
    file_name = 'EJEMPLO DE PRUEBA'
    file_ass = file_name + '.ass'
    instructions, data = text_reader(file_ass)
    memory_file(data, file_name)
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
        instructions, data = text_reader(file_ass)
        #print(f'Linea 475: instruction = {instructions}')
        jumps = jump_dic(instructions)
        
        for instruction in instructions:
            instruction = jumps_direction_changer(instruction, jumps)
        is_declared, argument = undeclared_variable_detector(instructions, data)
        if is_declared == False:
            print(f'Error, se utilizan variables no declaradas en el apartado Data: {argument}')
        elif is_declared == True:
            #print(f'Linea 479: instruction = {instructions}')    
            instructions = data_direction_changer(instructions, data)
            #print(f'Linea 481: instruction = {instructions}')
            literal_list, out_of_range, literal_out = literal_list_generator (instructions)
            if out_of_range == True:
                print(f'Error, Un literal esta fuera del rango permitido {literal_out}') 
            else: 
                print(f'Data :')
                for dat in data:
                    print(dat)
                print(f'Code :')
                for instruction in instructions:
                    print(instruction)

                for instruction in instructions:
                    instruction = dir_int_changer(instruction)
                #print(f'Linea 485: instruction = {instructions}')
                output_file_writer(instructions, opc, literal_list, file_name)
                print('Archivo creado con exito!')

main(operations)