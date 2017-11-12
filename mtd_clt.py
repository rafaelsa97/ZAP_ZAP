# -*- coding: utf-8 -*-

# ============================ ZAP ZAP - Cliente ============================
# Programa de chat desenvolvido para a disciplina de Redes de Computadores
# UNIVERSIDADE FEDERAL DE MINAS GERAIS
# Desenvolvido por Bhryan Henderson Lopes Perpétuo e Rafael Santos de Almeida
# Novembro de 2017
# ===========================================================================

import struct
import sys
import socket

# Classe para formatar as cores do texto de apresentacao e lista_comandos
class bcolors:
    HEADER = '\033[95m'  # Rosa claro
    OKBLUE = '\033[94m'  # Azul
    OKGREEN = '\033[92m' # Verde
    WARNING = '\033[93m' # Amarelo
    FAIL = '\033[91m'    # Vermelho
    ENDC = '\033[0m'     # Branco

# apresentacao()
# Mensagem inicial
# Saída: ---//---
def apresentacao():
    print bcolors.OKBLUE + "\n\n███████╗ █████╗ ██████╗     ███████╗ █████╗ ██████╗ " + bcolors.ENDC
    print bcolors.OKBLUE + "╚══███╔╝██╔══██╗██╔══██╗    ╚══███╔╝██╔══██╗██╔══██╗" + bcolors.ENDC
    print bcolors.OKBLUE + "  ███╔╝ ███████║██████╔╝      ███╔╝ ███████║██████╔╝" + bcolors.ENDC
    print bcolors.OKBLUE + " ███╔╝  ██╔══██║██╔═══╝      ███╔╝  ██╔══██║██╔═══╝ " + bcolors.ENDC
    print bcolors.OKBLUE + "███████╗██║  ██║██║         ███████╗██║  ██║██║     " + bcolors.ENDC
    print bcolors.OKBLUE + "╚══════╝╚═╝  ╚═╝╚═╝         ╚══════╝╚═╝  ╚═╝╚═╝     \n" + bcolors.ENDC
    print bcolors.OKBLUE + "Por Bhryan Henderson e Rafael Santos de Almeida\n" + bcolors.ENDC

# lista_comandos()
# Imprime a lista de comandos do programa
# Saída: ---//---
def lista_comandos():
    print bcolors.FAIL + "------- COMANDOS -------"
    print bcolors.WARNING + "CREQ: Lista os clientes online\nCONECTA \"número\": Conecta a um cliente online"
    print bcolors.WARNING + "FLW: Desconecta\nIDF: Imprime o nº de identificador próprio do cliente"
    print bcolors.WARNING + "HELP: Imprime a lista de comandos novamente\n" + bcolors.ENDC

# cria_socket_e_conecta(número de IP,número do PORTO)
# Cria um socket e o conecta ao servidor
# Saída: socket com o servidor, caso haja sucesso
def cria_socket_e_conecta(IP,PORTO):
    # Cria um soquete com o servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta ao servidor
    if s:
        s.connect((IP, PORTO))
    else: # Encerra caso haja erro
        print "Não foi possível conectar ao servidor"
        s.close
        sys.exit(0)
    return s

# msg_OI(socket ligado ao servidor)
# Envia mensagem ao servidor requisitando número de identificador
# Saída: número de identificador, caso haja sucesso
def msg_OI(s):
    s.send(struct.pack('!4H',3,0,65535,0)) # Envia requisião OI, se identificando ao servidor
    idf = s.recv(8)                        # Recebe confirmação do servidor
    # Confere se requisição foi obtida com sucesso:
    if not idf:
        print "O programa não pôde obter o número identificador com o servidor."
        s.close
        sys.exit(0)
    s_aux = struct.unpack('!4H',idf) # Desempacota confirmação do servidor
    idf =  int(s_aux[2])
    if s_aux[0] == 1: # Confere se recebeu um ok do servidor
        if idf == 0 or idf == 65535: # Confere se recebeu um núm. de identificador inválido
            print "ERRO!\nCliente recebeu número de identificador inválido"
            s.close
            sys.exit(0)
        print "Identificador: " + str(idf)
        sys.stdout.write('-> '); sys.stdout.flush()
        return idf
    else:
        print "Falha na atribuicao de numero de identificador pelo servidor"
        s.close
        sys.exit(0)

# conecta_a_destinatario(núm. identificador digitado pelo usuário para conectar, identificador próprio do cliente)
# Descobre se é possível conectar ao cliente descrito pelo usuário
# Saída: identificador do destinatário em caso de sucesso, identificador do servidor em caso de erro
def conecta_a_destinatario(aux,id_proprio):
    if aux == id_proprio:
        print "ERRO!\nNão é possível enviar mensagem para você mesmo. Conecte a outro cliente"
        return 65535
    elif aux == 65535:
        print "ERRO!\nNão é possível enviar mensagem para este número (identificador do servidor)"
        return 65535
    else:
        id_dest = aux
        print "Conectado a cliente " + str(id_dest)
        return id_dest

# msg_MSG(string com a mensagem digitada, núm. do identif. do cliente, socket com o serv., núm. do identif. do destinatário, número de sequência)
# Insere cabecalho e envia mensagem digitada pelo usuário para o servidor
# Saída: número de sequência das mensagens
def msg_MSG(msg, id_cliente, s, id_dest,num_seq):
    if not msg:
        return num_seq
    # Cria cabecalho
    tipo = 5
    num_seq = num_seq + 1 # Incrementa o número de sequência
    tipo_idf = struct.pack('!4H', tipo, id_cliente, id_dest,num_seq) # Encapsulamento do cabeçalho
    tam = struct.pack('!H',len(msg)) # Encapsulamento do tamanho da mensagem
    # Recebe e empacota o payload
    s_aux = ""
    for i in msg:
        s_aux = s_aux + struct.pack('!B',ord(i))
    s.send(tipo_idf + tam + s_aux)
    try:
        s.settimeout(5)
        tipo, idf_org, idf_dst, num_seq_rec = struct.unpack('!4H',s.recv(8))
        confirm = trata_ok(tipo,num_seq,s)
        if confirm == 2:
            print "ERRO!\nNão foi possível enviar mensagem. Confira se o destinatário está conectado com a função CREQ"
    except socket.timeout:
        print "Não foi possível obter a confirmação de recebimento com o servidor (tempo excessivo)"
        s.close
        sys.exit(0)
    return num_seq

# msg_FLW(identificador do cliente, socket ligado ao servidor, identificador do destinatário, número de sequência)
# Envia mensagem ao servidor informando saída
# Saída: ---//---
def msg_FLW(id_cliente,s,id_dest,num_seq):
    # Cria cabecalho
    tipo = 4
    tipo_idf = struct.pack('!4H', tipo, id_cliente, id_dest,num_seq)
    s.send(tipo_idf)
    try:
        s.settimeout(5)
        tipo, idf_org, idf_dst, num_seq_rec = struct.unpack('!4H',s.recv(8))
        confirm = trata_ok(tipo,num_seq,s)
        if confirm == 1: # Recebeu um OK
            print "Conexão encerrada."
            s.close
            sys.exit(0)
        elif confirm == 2: # Recebeu um ERRO
            print "ERRO!\nNão foi possível encerrar a conexão. Tente novamente"
    except socket.timeout:
        print "ERRO!\nNão foi possível obter a confirmação com o servidor. Tente novamente"

# msg_CREQ(identificador do cliente, socket ligado ao servidor, número de sequência)
# Envia requisição para receber lista de clientes conectados ao servidor e os imprime na tela
# Saída: ---//---
def msg_CREQ(idf,s,num_seq):
    # Cria cabecalho
    tipo_CREQ = 6
    idf_serv = 65535
    # Envia requisição da lista:
    cabec = struct.pack('!4H', tipo_CREQ, idf, idf_serv,num_seq)
    s.send(cabec)
    buf = s.recv(10) # Recebe cabec + tamanho da lista de clientes
    if buf:
        tipo, idf_org, idf_dst, num_seq, tam_lista = struct.unpack('!5H',buf)
        # Confere se recebeu mensagem tipo CLIST
        if tipo != 7:
            aux = s.recv(1024) # Recebe quaisquer outros pacotes que o servidor chegue a enviar
            print "ERRO!\nPacote recebido de tipo diferente de CLIST."
            # Envia uma mensagem de erro ao servidor
            s.send(struct.pack('!4H',2,idf,idf_serv,num_seq))
        else:
            print "---------- LISTA DE CLIENTES ----------"
            for i in range (tam_lista):
                buf2 = struct.unpack('!H',s.recv(2))
                print "Cliente " + str(buf2[0])
            s.send(struct.pack('!4H',1,idf,idf_serv,num_seq)) # Envia um ok para o servidor
    else:
        print "ERRO!\nNão foi possível receber a lista de clientes"
        # Envia uma mensagem de erro ao servidor
        s.send(struct.pack('!4H',2,idf,idf_serv,num_seq))

# digita_mensagem()
# Obtém a mensagem enviada pelo usuário através do terminal
# Saída: mensagem digitada pelo usuário
def digita_mensagem():
    buf = sys.stdin.readline()
    # Controla o num. max. de caracteres da mensagem
    while len(buf) > 400:
        print "Atencao! Mensagem limitada a 400 caracteres.\nDigite novamente sua mensagem"
        buf = raw_input("-> ")
    # Caso o stdin leia um enter, o enter "\n" é removido da string
    mensagem = buf.replace("\n","")
    return mensagem

# recebe_MSG(cabeçalho da mensagem recebida, socket do cliente com o serv., id. do cliente, id. do serv., número de sequência)
# Recebe mensagem encaminhada pelo servidor
# Saída: ---//---
def recebe_MSG(data,s,id_proprio,idf_serv,num_seq):
    tipo, id_remet, id_dest, num_seq, tam = struct.unpack('!5H', data)
    # Recebe e desempacota o payload da mensagem:
    mensagem = ""
    for i in range(tam):
        byte = struct.unpack('!B', s.recv(1))
        mensagem = mensagem + str(chr(byte[0]))
    # Envia um ok para o servidor
    s.send(struct.pack('!4H',1,id_proprio,idf_serv,num_seq))
    print "\n" + str(id_remet) + " diz: " + mensagem

# trata_ok(identificador do tipo da msg recebida, número de sequência esperado, socket com o servidor)
# Confere se recebeu um OK do servidor e se ele se trata do num. sequência esperado
# Saída: 1 caso tenha recebido um OK, 2 caso tenha recebido um ERRO
def trata_ok(tipo,num_seq,s):
    # Confere se recebeu erro
    if tipo == 1: # Recebido um OK
        return 1
    elif tipo == 2: # Recebido um ERRO
        return 2
    # Confere se a confirmação recebida é relativa à mensagem de mesmo num. de sequência
    if num_seq_rec != num_seq:
        print "Confirmação recebida do servidor com número de sequência não esperado."
        print "Número de sequência recebido: " + num_seq_rec
        print "Número de sequência esperado: " + num_seq_rec
        s.close
        sys.exit(0)
