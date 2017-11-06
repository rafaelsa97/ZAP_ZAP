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
while 1:
    id_dest = 0
    # Função select
    socket_list = [sys.stdin, s]
    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
    for sock in ready_to_read:
        if sock == s:
            # Cliente recebe mensagem
            data = sock.recv(8)
            if not data :
                print 'Cliente desconectado'
                sys.exit()
            else :
                #print data
                tipo, id_remet, id_dest, tam = struct.unpack('!4H', data)
                mensagem = ""
                for i in range(tam):
                    byte = struct.unpacl('!B', s.recv(1))
                    mensagem = mensagem + str(chr(byte[0]))
                sys.stdout.write(mensagem)
                sys.stdout.write('-vamo ver se aparece> '); sys.stdout.flush()
        else :
            # Cliente envia mensagem
            mensagem = mtd_clt.recebe_mensagem()
            if mensagem == "FLW":
                flw_result = mtd_clt.msg_FLW(id_proprio,s,id_dest)
                s.close
                sys.exit()
                break
            elif mensagem == "CREQ":
                mtd_clt.msg_CREQ(id_proprio,s)
            elif mensagem[0:7] == "CONECTA" and id_dest == 0:
                id_dest = int(mensagem[8:])
            else:
                msg_result = mtd_clt.msg_MSG(mensagem,id_proprio,s,id_dest)
