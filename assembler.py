## LABORATÓRIO 1 OAC

registradores = ['$0', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3', '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
         '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7', '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']

registradores_num = ['$0', '$1', '$2', '$3', '$4', '$5', '$6', '$7', '$8', '$9', '$10', '$11', '$12', '$13', '$14', '$15',
         '$16', '$17', '$18', '$19', '$20', '$21', '$22', '$23', '$24', '$25', '$26', '$27', '$28', '$29', '$30', '$31']

tipo_r = ['sll', 'srl', 'sra', 'srav', 'jr', 'jalr', 'mfhi', 'clo', 'mflo', 'mult', 'multu', 'div', 'divu', 'add', 'addu', 'sub', 'subu', 'and', 'or', 'xor', 'nor', 'slt', 'sltu']
funct_r = [0x00, 0x02, 0x03, 0x07, 0x08, 0x09, 0x10, 0x11, 0x12, 0x18, 0x19, 0x1a, 0x1b, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x2a, 0x2b]

tipo_i = ['beq', 'bne', 'addi', 'addiu', 'lw', 'sw', 'andi', 'ori', 'xori', 'lui']
opcode_i = [0x04, 0x05, 0x08, 0x09, 0x23, 0x2b, 0x0c, 0x0d, 0x0e, 0x0f]

tipo_j = ['j', 'jal']

opcode_j = [0x02, 0x03]

special = ['bgez', 'bgezal', 'madd', 'msubu']

label_list = []
label_endereco = []

instructions = tipo_i + tipo_r + tipo_j+ special
instructions.append('li')

def returnHexCode(name, arg1, arg2, arg3, funct='000000', opcode = '000000', shamt = '00000'):
    txt = ''

    if name in ['add' , 'addu' , 'sub' , 'slt' , 'srav' , 'sub' , 'subu'
    , 'and' , 'or' , 'nor' , 'xor']:
        arg1 = str(f'{arg1:05b}')
        arg2 = str(f'{arg2:05b}')
        arg3 = str(f'{arg3:05b}')
        txt += opcode + arg2 + arg3 + arg1 + shamt + funct

    if name in ['addi' , 'andi' , 'ori' , 'xori']:
        arg1 = str(f'{arg1:05b}')
        arg2 = str(f'{arg2:05b}')
        arg3 = str(f'{arg3:016b}')
        txt += opcode + arg2 + arg1 + arg3

    if name in ['sll' , 'sra' , 'srl']:
        arg1 = str(f'{arg1:05b}')
        arg2 = str(f'{arg2:05b}')
        arg3 = str(f'{arg3:05b}')
        txt += opcode + '00000' + arg2 + arg1 + arg3 + funct

    if name in ['srav']:
        arg1 = str(f'{arg1:05b}')
        arg2 = str(f'{arg2:05b}')
        arg3 = str(f'{arg3:05b}')
        txt += opcode + arg3 + arg2 + arg1 + shamt + funct

    if name in ['sw','lw']:
        arg1 = str(f'{arg1:05b}')
        arg3 = str(f'{arg3:05b}')
        arg2 = str(f'{arg2:016b}')
        txt += opcode + arg3 + arg1 + arg2

    if name in ['lui']:
        arg1 = str(f'{arg1:05b}')
        arg2 = str(f'{arg2:016b}')
        txt += opcode + '00000' + arg1 + arg2

    if name in ['j', 'jal']:  #???
        arg1 = str(f'{arg1:026b}')
        txt += opcode + arg1

    if name in ['jalr']:
        arg1 = str(f'{arg1:05b}')
        txt += opcode + arg1 + '00000' + '10000' + shamt + '100000'

    if name == 'jr':
        arg1 = str(f'{arg1:05b}')
        txt += opcode + arg1 + '00000' + '00000' + shamt + funct

    if name in ['beq', 'bne']:
        arg1 = str(f'{arg1:05b}')
        arg2 = str(f'{arg2:05b}')
        arg3 = str(f'{arg3:016b}')
        txt += opcode + arg1 + arg2 + arg3
    
    if name in ['mult' , 'div']:
        arg1 = str(f'{arg1:05b}')
        arg2 = str(f'{arg2:05b}')
        txt += opcode + arg1 + arg2 + '0000000000' + funct

    if name in ['mfhi', 'mflo']:
        arg1 = str(f'{arg1:05b}')
        txt += opcode + '0000000000' + arg1 + shamt + funct

    if name in ['bgez', 'bgezal']:
        opcode = '000001'
        arg1 = str(f'{arg1:05b}')
        arg2 = str(f'{arg2:016b}')
        funct = '00001'
        if name == 'bgez':
            funct = '00001'
        else:
            funct = '10001'
        txt += opcode + arg1 + funct + arg2
    
    if name in ['clo']:
        arg1 = str(f'{arg1:05b}')
        arg2 = str(f'{arg2:05b}')
        txt += '011100' + arg2 + '00000' + arg1 + '00000' + '100001'

    if name in ['msubu', 'madd']:
        arg1 = str(f'{arg1:05b}')
        arg2 = str(f'{arg2:05b}')
        if name == 'msubu':
            funct = '000101'
        else:
            funct = '000000'
        txt += '011100' + arg1 + arg2 + '00000' + '00000' + funct
    txt = int(txt, 2)
    txt = f'{txt:08x}'
    return txt
    
        
arq = input('Insira o nome do arquivo de leitura (arq.asm):\n')
#arq = 'example_saida.asm'
while True:
    try:
        f = open(arq, 'r')  #nome do arquivo de entrada
        break
    except:
        print('Não foi possível abrir o arquivo')
        arq = input('Insira o nome do arquivo (arquivo.asm):\n')


lines = f.readlines()
f.close()

endereco_text = 0x00400000    #Endereçamento de instruções começa em 0x00400000
endereco_data = 0x10010000    #Endereçamento de data começa em 0x10010000
line_count = 0
output = ''
istext = False
isdata = False
labelRead = True
saida_text = 'DEPTH = 4096;\nWIDTH = 32;\nADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n\n'
saida_data = 'DEPTH = 16384;\nWIDTH = 32;\nADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\nCONTENT\nBEGIN\n\n'


for line in lines:
    line_count+=1
    notInst = False
    if line == '.text\n':
        istext = True
        isdata = False
        continue
    
    if line == '.data\n':
        isdata = True
        istext = False
        continue

    if isdata and not istext: #quando é .data
        if line == '.text\n':
            istext = True
            isdata = False
            continue

        if line.find(':') != -1: #encontra o dado
            line = line.split()
            line.pop(0)
            line.pop(0)

            for value in line:
                value = value.replace(',','')
                saida_data += f'{endereco_data:08x}' + ' : ' + f'{int(value):08x}' + ';\n'
                endereco_data += 4



    if istext and not isdata:
        if line == '.data\n':
            istext = False
            isdata = True
            continue

        if labelRead:
            for i in range(line_count-1, len(lines)):
                if lines[i].find(':') != -1:
                    labelName = lines[i].split(':')[0]
                    label_list.append(labelName)
                    n_label = n_label = '0x{:08x}'.format(endereco_text)
                    label_endereco.append(n_label)
                    lines[i] = lines[i].replace(lines[i], lines[i].split(':')[1]) #tira a parte antes do ':', importante para caso haja instrução após a label
                    

                elif lines[i] != '\n':
                    if lines[i].split()[0] == 'li': #caso tenha instrução 'li' pula adiciona um address a mais
                        endereco_text += 4
                    endereco_text += 4
            endereco_text = 0x00400000
            labelRead = False
        args = line.split() #separa os argumentos da instrução
        if not args: #se não há argumentos então a linha é pulada
            continue
        arg1 = 0
        arg2 = 0
        arg3 = 0

        for i in range(len(args)): #varre os argumentos
            if i == 0:
                inst = args[0] # 1º argumento: instrução
                if inst not in instructions: #verifica se a instrução está no banco de instruções
                    #print(inst + ' not instruction')
                    notInst = True

            if i == 1:
                if ',' in args[1]:
                    arg1 = args[1].replace(',','')
                else:
                    arg1 = args[1]
                    
            if i == 2:
                if '(' in args[2]: # verifica se o arg2 é da forma a(b)
                    aux = args[2].split('(')
                    arg2 = aux[0]
                    arg3 = aux[1].replace(')','')
                    break
                else:
                    arg2 = args[2].replace(',','')
            if i == 3:
                arg3 = args[3]
        if notInst:
            notInst = False
            continue

        ### arg2 ou arg3 é hexadecimal? ###
        if '0x' in str(arg2):
            arg2 = int(arg2, 16)
        if '0x' in str(arg3):
            arg3 = int(arg3, 16)

        ### argumento é um registrador? ###
        if arg1 in registradores:
            arg1 = registradores.index(arg1)
        elif arg1 in registradores_num:
            arg1 = registradores_num.index(arg1)
        if arg2 in registradores:
            arg2 = registradores.index(arg2)
        elif arg2 in registradores_num:
            arg2 = registradores_num.index(arg2)
        if arg3 in registradores:
            arg3 = registradores.index(arg3)
        elif arg3 in registradores_num:
            arg3 = registradores_num.index(arg3)

        ### caso a instrução não seja do tipo J tratar os args pra int ###
        if inst not in tipo_j:
            arg1 = int(arg1)
            if inst not in ['bgez', 'bgezal']:
                arg2 = int(arg2)
            else:
                if arg2 in label_list:
                    arg2 = int(label_endereco[label_list.index(arg2)], 16)
                    arg2 = int((arg2 - endereco_text)/4)

                    if arg2 <= 0:
                        arg2 = int('0xffffffff', 16) - abs(arg2)
                        arg2 = int(bin(arg2 & 0xffff), 2)
                    else:
                        arg2 -= 1
                else:
                    arg2 = int(arg2, 16)
            if inst not in ['bne', 'beq']:
                arg3 = int(arg3)
            else:
                if arg3 in label_list:
                    arg3 = int(label_endereco[label_list.index(arg3)], 16)
                    arg3 = int((arg3 - endereco_text)/4)

                    if arg3 <= 0:
                        arg3 = int('0xffffffff', 16) - abs(arg3)
                        arg3 = int(bin(arg3 & 0xffff), 2)
                    else:
                        arg3 -= 1
                else:
                    arg3 = int(arg3, 16)
    

        ### instrução tipo R recebe funct ###
        if inst in tipo_r:
            i = tipo_r.index(inst)
            result = returnHexCode(inst, arg1, arg2, arg3, funct=str( f'{funct_r[i]:06b}' ))

        ### instrução tipo I recebe opcode ###
        if inst in tipo_i:
            i = tipo_i.index(inst)
            result = returnHexCode(inst, arg1, arg2, arg3, opcode=str( f'{opcode_i[i]:06b}' ))

        ### instrução tipo especial ###
        if inst in special:
            result = returnHexCode(inst, arg1, arg2, arg3)

        if inst in tipo_j:
            if arg1 in label_list:
                i = label_list.index(arg1)
                arg1 = int(label_endereco[i], 16)
            else:
                arg1 = int(arg1, 16)
            i = tipo_j.index(inst)
            arg1 = int(arg1/4)
            result = returnHexCode(inst, arg1, arg2, arg3, opcode=str( f'{opcode_j[i]:06b}' ))

        ### tratar pseudoinstrução 'li' ##
        if inst == 'li':
            a = int(bin(arg2 >> 16), 2)
            b = int(bin(arg2 & 0xffff), 2)
            inst = 'lui'
            result = returnHexCode(inst, 1, a, arg3, opcode=str( f'{opcode_i[tipo_i.index(inst)]:06b}' ))
            saida_text += f'{endereco_text:08x}' + ' : ' + result + '; % ' + str(line_count) + ': ' + line.split('\n')[0] + ' %\n'
            endereco_text += 4
            inst = 'ori'
            result = returnHexCode(inst, arg1, 1, b , opcode=str( f'{opcode_i[tipo_i.index(inst)]:06b}' ))
            saida_text += f'{endereco_text:08x}' + ' : ' + result + ';\n'
            endereco_text += 4
            continue
        
        saida_text += f'{endereco_text:08x}' + ' : ' + result + '; % ' + str(line_count) + ': ' + line.split('\n')[0] + ' %\n'
        endereco_text += 4

saida_text += '\nEND;'
saida_data += '\nEND;'

file_data = arq.replace('.asm', '_data.mif')
file_text = arq.replace('.asm', '_text.mif')

try:
    f = open(file_data, 'w')
    f.write(saida_data)
    f.close()
    print('Arquivo ' + file_data + ' criado.')
except:
    print('Falha ao criar o arquivo .mif de dados')
try:    
    f = open(file_text, 'w')
    f.write(saida_text)
    f.close()
    print('Arquivo ' + file_text + ' criado.')
except:
    print('Falha ao criar o arquivo .mif de instruções')

#print(saida_text)
