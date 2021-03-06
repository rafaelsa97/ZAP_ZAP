# -*- coding: utf-8 -*-

# ============================ ZAP ZAP - Cliente ============================
# Programa de chat desenvolvido para a disciplina de Redes de Computadores
# UNIVERSIDADE FEDERAL DE MINAS GERAIS
# Desenvolvido por Bhryan Henderson Lopes Perpétuo e Rafael Santos de Almeida
# Novembro de 2017
# ===========================================================================

# CABEÇALHO:
# |tipo_da_msg || id_da_origem || id_do_destino || num_da_sequencia|

import sys
import socket
import struct
import mtd_clt
import select

# Mensagens iniciais:
mtd_clt.apresentacao()
mtd_clt.lista_comandos()
# Endereco de IP  e porto de comunicacao ouvido pelo cliente:
IP = sys.argv[2]
PORTO = int(sys.argv[3])
idf_serv = 65535 # Número de identificador do servidor
id_dest  = 65535 # Número de identificador do destinatário
# Cria socket com o servidor
s = mtd_clt.cria_socket_e_conecta(IP,PORTO)
# Obtem num. identificador com o servidor
id_proprio = mtd_clt.msg_OI(s)
num_seq = 0 # Número de sequência das mensagens

while 1:
    # Função select:
    socket_list = [sys.stdin, s]
    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
    for sock in ready_to_read:
        if sock == s:
            # Cliente recebe mensagem
            data = sock.recv(10)
            if not data :
                print 'Cliente não pôde receber mensagem.'
                s.close
                sys.exit(0)
            else :
                mtd_clt.recebe_MSG(data,s,id_proprio,idf_serv,num_seq) # Recebe e printa mensagem recebida pelo serv.
        else :
            mensagem = mtd_clt.digita_mensagem() # Obtém comando/mensagem digitado pelo usuário
            if mensagem == "FLW": # Encerra conexão
                mtd_clt.msg_FLW(id_proprio,s,id_dest,num_seq)
            elif mensagem == "CREQ": # Requisita ao servidor a lista de clientes conectados
                mtd_clt.msg_CREQ(id_proprio,s,num_seq)
            elif mensagem == "HELP": # Imprime a lista de comandos
                mtd_clt.lista_comandos()
            elif mensagem == "IDF": # Imprime o número de identificador próprio
                print "Identificador: " + str(id_proprio)
            elif mensagem[0:8] == "CONECTA ": # Seleciona com qual cliente vai se conectar
                id_dest = mtd_clt.conecta_a_destinatario(int(mensagem[8:]),id_proprio)
            else: # Envia mensagem ao cliente já conectado
                if id_dest != 65535: # Confere se o cliente definiu com qual cliente irá se comunicar (se usou CONECTA)
                    num_seq = mtd_clt.msg_MSG(mensagem,id_proprio,s,id_dest,num_seq)
                else:
                    print "ERRO AO ENVIAR MENSAGEM!\nDigite 'CONECTA' e o número do cliente que se deseja conectar."
        sys.stdout.write("-> "); sys.stdout.flush()
