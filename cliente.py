# -*- coding: utf-8 -*-

# CABECALHO:
# |tipo_da_msg || id_da_origem || id_do_destino || num_da_sequencia|

import socket
import struct
import mtd_clt

print "ZAP ZAP initiated"
# Endereco de IP  e porto de comunicacao ouvido pelo cliente:
IP = '177.15.163.236'
PORTO = 51515
# Conecta ao servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORTO))

while 1:
    # Obtem num. identificador com o servidor
    idf = mtd_clt.msg_OI(s)
    if idf == 0:
        s.close
        break

    while 1:
        print("Digte sua mensagem:")
        mensagem = raw_input("-> ")
        if mensagem == "FLW":
            flw_result = mtd_clt.msg_FLW(idf,s)
            #s.send(struct.pack('!i',4010))
            break
        # Controla o num. max. de caracteres da mensagem
        while len(mensagem) > 400:
            print "Atencao! Mensagem limitada a 400 caracteres.\nDigite novamente sua mensagem"
            mensagem = raw_input("-> ")
        msg_result = mtd_clt.msg_MSG(mensagem,idf,s)
    # Encerra conexao
    s.close
    break
