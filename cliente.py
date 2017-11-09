# -*- coding: utf-8 -*-

# CABECALHO:
# |tipo_da_msg || id_da_origem || id_do_destino || num_da_sequencia|

import sys
import socket
import struct
import mtd_clt
import select

print "ZAP ZAP initiated"
# Endereco de IP  e porto de comunicacao ouvido pelo cliente:
IP = sys.argv[2]
PORTO = int(sys.argv[3])
# Cria um soquete com o servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conecta ao servidor
try:
    s.connect((IP, PORTO))
except:
    print "Não foi possível conectar ao servidor"
    sys.exit()
# Obtem num. identificador com o servidor
id_proprio = mtd_clt.msg_OI(s)
idf_serv = 65535
id_dest = 65535 # Número de identificador do destinatário
while 1:
    # Função select
    socket_list = [sys.stdin, s]
    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
    for sock in ready_to_read:
        if sock == s:
            # Cliente recebe mensagem
            data = sock.recv(8)
            if not data :
                print 'Cliente não pôde receber mensagem.'
                sys.exit(0)
            else :
                #print data
                tipo, id_remet, id_dest, tam = struct.unpack('!4H', data)
                mensagem = ""
                for i in range(tam):
                    byte = struct.unpack('!B', s.recv(1))
                    mensagem = mensagem + str(chr(byte[0]))
                # Envia um ok para o servidor
                s.send(struct.pack('!4H',1,id_proprio,idf_serv,0))
                sys.stdout.write('-vamo ver se aparece> '); sys.stdout.flush()
                sys.stdout.write(mensagem)
        else :
            # Cliente envia mensagem
            mensagem = mtd_clt.digita_mensagem()
            if mensagem == "FLW": # Encerra conexão
                flw_result = mtd_clt.msg_FLW(id_proprio,s,id_dest)
                s.close
                sys.exit(0)
                break
            elif mensagem == "CREQ": # Requisita ao servidor a lista de clientes conectados
                mtd_clt.msg_CREQ(id_proprio,s)
            elif mensagem[0:7] == "CONECTA": # Seleciona com qual cliente vai se conectar
                id_dest = int(mensagem[8:])
                print "id_dest: " + str(id_dest)
            else: # Envia mensagem ao cliente já conectado
                if id_dest != 65535:
                    msg_result = mtd_clt.msg_MSG(mensagem,id_proprio,s,id_dest)
                    print "id_dest: " + str(id_dest)
                else:
                    print "ERRO AO ENVIAR MENSAGEM!\nDigite 'CONECTA' e o número do cliente que se deseja conectar."
                    print "id_dest: " + str(id_dest)
