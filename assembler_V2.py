import re
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

def opcodes():
    operations = ['MOV','ADD','SUB','AND','OR','NOT','XOR','SHL','SHR','INC',
            'RST','CMP','JMP','JEQ','JNE','JGT','JLT','JGE','JLE','JCR','JOV',
            'CALL','RET','PUSH','POP']
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

def instruction_validator (instruction, len_instuctions, opc):
    #print(f'instruccion inicial : {instruction}')
    # RET instruction
    ins_trans = instruction[0]+' '
    if instruction[0] == 'RET':
        if len(instruction) != 1:
            arg = ','.join(instruction[1])
            return f'Instruccion invalida: {ins_trans}{arg} (92)' 
        if len(instruction) == 1:
            return True  

    # Non-existent instruction
    operations = ['MOV','ADD','SUB','AND','OR','NOT','XOR','SHL','SHR','INC',
            'RST','CMP','JMP','JEQ','JNE','JGT','JLT','JGE','JLE','JCR','JOV',
            'CALL','RET','PUSH','POP']
    
    if len(instruction) == 2:
        if type(instruction[1]) is list:
            arg = ','.join(instruction[1])
        elif  "#" in instruction[1]:
            arg = str(instruction[1])
        else: 
            arg = str(instruction[1])
        if instruction[0] not in operations:
            return f'Instruccion no existe: {ins_trans} {arg}'
    
    # number of arguments
    if instruction[0] == 'INC':
        if len(instruction[1]) != 1 and '(' not in instruction[1] :
            return f'Instruccion invalida (Cantidad de argumentos): {ins_trans}{arg} (114)'
    if instruction[0] == 'MOV' or instruction[0] == 'CMP':
        if len(instruction[1]) != 2:
            return f'Instruccion invalida (Cantidad de argumentos): {ins_trans}{arg} (116)'
    
    if len(instruction[1]) > 2 and type(instruction[1]) is list:
        return f'Instruccion invalida (Cantidad de argumentos): {ins_trans}{arg} (119)'
    
    # Add Literals and dir.
    if '(' in instruction[1]:
        if '(' in instruction[1] and '(A)' != instruction[1] :
            if '(B)' != instruction[1]:
                instruction.pop(1)
                instruction.insert(1, '(Dir)')
            else:
                instruction.pop(1)
                instruction.insert(1, '(B)')
        else:
            return 'No existe direccionamiento a través del registro A (132)'
            
    #print(f'instruccion 1 : {instruction}')

    if type(instruction[1]) is list:
        for i in range(len(instruction[1])):
            if instruction[1][i] != 'A' and instruction[1][i] != 'B':
                if  '(' in instruction[1][i] and '(A)' != instruction[1][i] and '(B)' != instruction[1][i]:
                    if '(B)' == instruction[1][i]:
                        pass
                    elif instruction[1][i] != '(A)':
                        instruction[1].pop(i)
                        instruction[1].insert(i, '(Dir)') 

                    else:
                        return 'No existe direccionamiento a través del registro A (147)'
                elif instruction[1][i] == '(B)':
                    pass
                else:
                    instruction[1].pop(i)
                    instruction[1].insert(i, 'Lit') 

    #print(f'instruccion 2 : {instruction}')

    #JUMP
    if 'J' in instruction[0]:
        arg = instruction[1]
        number = True
        try:
            int(arg)
        except:
            number = False

        if '#' in arg or number == True:
            arg = hex_to_dec(arg)
            if arg > len_instuctions:
                return f'Direccion fuera de rango: {ins_trans}{instruction[1]} (168)'
        else:
            return f'Direccion no valida: {ins_trans}{instruction[1]} (170)'
        if number == True:
            instruction.pop(1)
            instruction.insert(1, '(Dir)')

    #print(f'instruccion 3 : {instruction}')

    #Operations Chek
    if '(B)' == instruction[1]:
        arg = '(B)' 
    elif '#' not in instruction[1] and 'D' not in instruction[1] :
        arg = ','.join(instruction[1])
    else:
        arg = '(Dir)'
    ins_trans += arg
    
    #print(f'instruccion 4 : {instruction}')
    #print(ins_trans)
    if ins_trans in opc.keys():
        return True
    else:
        return f'Instruccion no existe: {ins_trans} (191)'
    
def dir_int_changer(instruction):
    if 'J' in instruction[0]:
        instruction.pop(1)
        instruction.insert(1, '(Dir)')
    if '(' in instruction[1] and '(A)' != instruction[1] and '(B)' != instruction[1]:
        instruction.pop(1)
        instruction.insert(1, '(Dir)')
    
    if type(instruction[1]) is list:
        for i in range(len(instruction[1])):
            if instruction[1][i] != 'A' and instruction[1][i] != 'B':
                if '(' in instruction[1][i] and '(A)' != instruction[1][i] and '(B)' != instruction[1][i]:
                    instruction[1].pop(i)
                    instruction[1].insert(i, '(Dir)') 
                elif '(B)' == instruction[1][i]:
                    pass
                else:
                    instruction[1].pop(i)
                    instruction[1].insert(i, 'Lit') 
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

def directions_changer(instructions, data, jumps):
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
    
        elif 'J' in instruction[0] :
            try: 
                arg = jumps[instruction[1]]
                instruction.pop(1)
                instruction.append(str(arg))
            except:
                pass
        
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

def literal_list_generator (instructions):
    literal_list = []
    for instruction in instructions:
        
        arg = 0
        #print(f'instruction litral list {instruction}')
        if type(instruction[1]) is list:
            for arg in instruction[1]:
                if '#' in arg and '(' not in arg:
                    string = arg.replace("#", "")
                    arg = int(string, 16)
                else:
                    try:
                        arg = int(arg)
                    except:
                        arg = 0
                        pass
            
        else:
            try:
                arg = int(instruction[1]) 
            except:
                arg = 0
                pass
            
                
        if int(arg) < 256 :
            binary = str(format(arg,'b'))
            while len(binary) < 8:
                binary = '0'+binary
            
        else:
            binary = '00000000'
        literal_list.append(binary)  

    return literal_list

def main():
    errors = 0
    opc = opcodes()
    instructions, data = text_reader('p3_2-correccion2.ass')
    #print(f'Punto 1: {instructions}')
    jumps = jump_dic(instructions)
    #print('jumps:', jumps)
    directions_changer(instructions, data, jumps)
    lit_list = literal_list_generator(instructions)
    #print(lit_list)
    #print(f'Punto 2: {instructions}')
    len_instructions = len(instructions)
    count = 1
    for instruction in instructions:
        #print(f' inea {count} ->{instruction}')
        instruction_validation = instruction_validator(instruction, len_instructions, opc)
        if instruction_validation != True:
            print(f'Error en la linea {count} ->{instruction_validation}')
            errors += 1
        count += 1
    #print(f'Punto 3: {instructions}')
    if errors == 0:
        #print('data:', data)
        new_instrucitons = []
        for instruction in instructions:
            new_instrucitons.append(dir_int_changer(instruction))
        output_file_writer(new_instrucitons, opc, lit_list)
        print('Archivo creado con exito!')

main()