def text_reader (text_name):
    file = open(text_name)
    lines = file.readlines()
    instructions = []
    for i in lines:
        i = i.split()
        if len(i) == 2:
            if ',' in i[1]:
                i[1] = i[1].split(',')

        instructions.append(i)
    return instructions

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

    # RET instruction
    ins_trans = instruction[0]+' '
    if instruction[0] == 'RET':
        if len(instruction) != 1:
            arg = ','.join(instruction[1])
            return f'Instruccion invalida: {ins_trans}{arg}' 
        if len(instruction) == 1:
            return True  

    # Non-existent instruction
    operations = ['MOV','ADD','SUB','AND','OR','NOT','XOR','SHL','SHR','INC',
            'RST','CMP','JMP','JEQ','JNE','JGT','JLT','JGE','JLE','JCR','JOV',
            'CALL','RET','PUSH','POP']
    
    if len(instruction) == 2:
        if  "#" in instruction[1]:
            arg = str(instruction[1])
        elif type(instruction[1]) is list:
            arg = ','.join(instruction[1])
        else: 
            arg = str(instruction[1])
        if instruction[0] not in operations:
            return f'Instruccion no existe: {ins_trans} {arg}'
    
    # number of arguments
    if instruction[0] == 'INC':
        if len(instruction[1]) != 1 and instruction[1] != '(B)' and instruction[1] != '(Dir)':
            return f'Instruccion invalida (Cantidad de argumentos): {ins_trans}{arg}'
    if instruction[0] == 'MOV' or instruction[0] == 'CMP':
        if len(instruction[1]) != 2:
            return f'Instruccion invalida (Cantidad de argumentos): {ins_trans}{arg}'
    
    if len(instruction[1]) > 2 and type(instruction[1]) is list:
        return f'Instruccion invalida (Cantidad de argumentos): {ins_trans}{arg}'
    
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
            return 'No existe direccionamiento a través del registro A'
    if type(instruction[1]) is list:
        for i in range(len(instruction[1])):
            if instruction[1][i] != 'A' and instruction[1][i] != 'B':
                if  '(' in instruction[1][i] and '(A)' != instruction[1][i] and '(B)' != instruction[1][i]:
                    if instruction[1][i] != '(A)':
                        instruction[1].pop(i)
                        instruction[1].insert(i, '(Dir)') 
                    else:
                        return 'No existe direccionamiento a través del registro A'
                else:
                    instruction[1].pop(i)
                    instruction[1].insert(i, 'Lit') 
    
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
                return f'Direccion fuera de rango: {ins_trans}{instruction[1]}'
        else:
            return f'Direccion no valida: {ins_trans}{instruction[1]}'
        if number == True:
            instruction.pop(1)
            instruction.insert(1, '(Dir)')

    #Operations Chek
    if '#' not in instruction[1] and 'D' not in instruction[1] and '(B)' not in instruction[1]:
        arg = ','.join(instruction[1])
    else:
        arg = '(Dir)'
    ins_trans += arg
    
    if ins_trans in opc.keys():
        return True
    else:
        return f'Instruccion no existe: {ins_trans}'

def output_file_writer(new_instrucitons, opc):
    file = open('out.txt', 'w')
    for instruction in new_instrucitons:
        ins_trans = instruction[0]+' '
        if type(instruction[1]) is list :
            arg = ','.join(instruction[1])
        else:
            arg = instruction[1]
        
        ins_trans += arg
        file.write(opc[ins_trans])
        file.write("\n")
    file.close()
   

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
                else:
                    instruction[1].pop(i)
                    instruction[1].insert(i, 'Lit') 
    return instruction


def main():
    errors = 0
    opc = opcodes()
    instructions = text_reader('p3-ej_incorrecto (1).ass')
    len_instructions = len(instructions)
    count = 1
    for instruction in instructions:
        instruction_validation = instruction_validator(instruction, len_instructions, opc)
        if instruction_validation != True:
            print(f'Error en la linea {count} ->{instruction_validation}')
            errors += 1
        count += 1
    if errors == 0:
        new_instrucitons = []
        for instruction in instructions:
            new_instrucitons.append(dir_int_changer(instruction))
        output_file_writer(new_instrucitons, opc)

            
        

main()