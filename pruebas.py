# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 17:34:08 2021

@author: lucaz
"""
'''''
import re 
file = open('p3F_1.ass')
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
        
jumps = {}
for line in instructions:
    if ':' in line[0]:
        index = instructions.index(line)
        word = line[0]
        word = re.sub(':', '',word)
        jumps[word] = index
        instructions.pop(index)


for instruction in instructions:
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
   
    elif 'J' in instruction[0] or 'CEQ' in instruction[0]:
        arg = jumps[instruction[1]]
        instruction.pop(1)
        instruction.append(arg)
    
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
                    
                    

literal_list = []
for instruction in instructions:
    arg = 0
    if type(instruction[1]) is list:
        for arg in instruction[1]:
            print(arg)
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
        
            
    if int(arg) < 256:
        binary = str(format(arg,'b'))
        while len(binary) < 8:
            binary = '0'+binary
        
    else:
        binary = '00000000'
                    
    literal_list.append(binary)
                    
'''               

print(int('(3)'))               
                    
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
            elif instruction[1][0] == 'B':
                b = int(b) + 1
            
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
                    
                    
                    