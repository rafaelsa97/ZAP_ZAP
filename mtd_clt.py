# -*- coding: utf-8 -*-
import struct
import sys

# msg_OI(socket ligado ao servidor)
# Envia mensagem ao servidor requisitando numero de identificador
# Saida: 0 caso haja falha, 1 caso tenha sucesso
def msg_OI(s):
    s.send(struct.pack('!4H',3,0,65535,0))
    idf = s.recv(8)
    # Confere se mensagem de resposta foi recebida
    if not idf:
        print "O programa nao pode obter o numero identificador com o servidor."
        return 0
    s_aux = struct.unpack('!4H',idf)
    idf =  int(s_aux[2])
    # Confere se recebeu um ok do servidor
    if s_aux[0] == 1:
        if idf == 0:
            print "Cliente recebeu número de identificador igual ao do servidor"
            s.close
        print "Identificador: " + str(idf)
        sys.stdout.write('-> '); sys.stdout.flush()
        return idf
    else:
        print "Falha na atribuicao de numero de identificador pelo servidor"
        return 0

# msg_MSG(string com a mensagem digitada, numero do identificador, socket de com. com o serv.)
# Insere cabecalho e envia mensagem digitada pelo user para o servidor
# Saida: 0 caso haja falha, 1 caso tenha sucesso
def msg_MSG(msg, id_cliente, s, id_dest):
    # Cria cabecalho
    tipo = 5
    tipo_idf = struct.pack('!3H', tipo, id_cliente, id_dest)
    # Encapsulamento do tamanho da mensagem
    tam = struct.pack('!H',len(msg))
    s_aux = ""
    for i in msg:
        s_aux = s_aux + struct.pack('!B',ord(i))
    s.send(tipo_idf + tam + s_aux)
    ok = struct.unpack('!4H',s.recv(8))
    while ok[0] != 1:
        ok = struct.unpack('!4H',s.recv(8))
    return 1

# msg_FLW(identificador do cliente, socket ligado ao servidor)
# Envia mensagem ao servidor informando saida
# Saida: 0 caso haja falha, 1 caso tenha sucesso
def msg_FLW(id_cliente,s,id_dest):
    # Cria cabecalho
    tipo = 4
    idf_serv = 65535
    tipo_idf = struct.pack('!4H', tipo, id_cliente, id_dest,0)
    s.send(tipo_idf)
    ok = struct.unpack('!4H',s.recv(8))
    while ok[0] != 1:
        ok = struct.unpack('!4H',s.recv(8))
    return 1

# msg_CREQ(identificador do cliente, socket ligado ao servidor)
# Envia requisição para receber lista de clientes conectados ao servidor e os imprime na tela
# Saida: 0 caso haja falha, 1 caso tenha sucesso
def msg_CREQ(idf,s):
    # Cria cabecalho
    tipo_CREQ = 6
    idf_serv = 65535
    cabec = struct.pack('!4H', tipo_CREQ, idf, idf_serv,0)
    s.send(cabec)
    buf = s.recv(10)
    if buf:
        tipo, idf_org, idf_dst, num_seq, tam_lista = struct.unpack('!5H',buf)
        print "---------- LISTA DE CLIENTES ----------"
        for i in range (tam_lista):
            buf2 = struct.unpack('!H',s.recv(2))
            print "Cliente " + str(buf2[0])
        # Envia um ok para o servidor
        s.send(struct.pack('!4H',1,idf,idf_serv,0))
    else:
        # Envia uma mensagem de erro ao servidor
        s.send(struct.pack('!4H',2,idf,idf_serv,0))

# recebe_mensagem()
# Obtém a mensagem enviada pelo usuário através do terminal
# Saida: mensagem digitada pelo usuário
def recebe_mensagem():
    buf = raw_input("-> ")
    # Caso o stdin leia um enter, o enter "\n" é removido da string
    mensagem = buf.replace("\n","")
    # Controla o num. max. de caracteres da mensagem
    while len(mensagem) > 400:
        print "Atencao! Mensagem limitada a 400 caracteres.\nDigite novamente sua mensagem"
        mensagem = raw_input("-> ")
    return mensagem
