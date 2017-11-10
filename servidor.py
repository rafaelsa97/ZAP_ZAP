# -*- coding: utf-8 -*-
#TP0 REDES - RAFAEL SANTOS DE ALMEIDA - 2015123614
#ENGENHARIA DE CONTROLE E AUTOMACAO - UFMG

import socket
import struct
import mtd_svr
import select
import sys

#Endereco IP e porto da comunicacao
IP = ''
PORTO = PORTO = int(sys.argv[2])

SOCKET_LIST = []
RECV_BUFFER = 4096
LISTA_ID = []
server_id = 65535

#Criacao do socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Aportando no porto do IP indicado
serversocket.bind((IP, PORTO))
#Esperando por conexao
serversocket.listen(65534)
#Colocar na lista de sockets, o socket do servidor
SOCKET_LIST.append(serversocket)

print "Chat server iniciado no porto: " + str(PORTO)

# Envia identificador para o cliente
while 1:

    ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

    for sock in ready_to_read:

                if sock == serversocket:
                        client,addr = serversocket.accept()
                        SOCKET_LIST.append(client)
                               # Recebe requisicao do cliente
                        print "Cliente (%s, %s) connectado" % addr
                        data = client.recv(8)
                        if not data:
                                break
                        else:
                                data = struct.unpack('!4H',data)
                                if data[0] == 3:
                                        new_client_id = mtd_svr.buscaID(SOCKET_LIST,client)
                                        if not new_client_id:
                                                break
                                        else:
                                                mtd_svr.ok(client,server_id,new_client_id)

                else:
                          # process data recieved from client,
                    try:
                        # receiving data from the socket.
                        data = sock.recv(10)
                        if data:
                            msg = ''
                            tipo,id_remet,id_dest,ordem,tam = struct.unpack("!5H",data)
                            for i in range(tam):
                                byte = struct.unpack('!B',sock.recv(1))
                                msg = msg + str(chr(byte[0]))
                            print tipo,id_remet,id_dest,ordem,tam,msg

                            #Mensagem de CREQ
                            if tipo == 6:
                                print "entrou no tipo CREQ"
                                mtd_svr.clist(sock,server_id,id_remet,SOCKET_LIST)
                                tipo,id_remet,id_dest,nothing = struct.unpack('!4H',sock.recv(8))
                                print tipo,id_remet,id_dest,nothing
                                if tipo == 2: # Se tiver erro...
                                    print "ERROR 404"

                            #Mensagem para outro
                            if tipo == 5:
                                print "entrou no tipo MSG"
                                mtd_svr.ok(sock,server_id,id_remet)
                                if id_dest == 0: #Broadcast
                                    # Empacota o payload
                                    s_aux = ""
                                    for c in msg:
                                        s_aux = s_aux + struct.pack('!B',ord(c))
                                    mtd_svr.encaminha_msg(SOCKET_LIST,data,s_aux,client)
                                else:
                                    dest =  procuraSock(id_dest,lista_socket)
                                    print "Socket destino: " + str(dest)
                                    if dest:
                                        dest.send(data)
                                        mtd_svr.ok(remet,65535,id_remet)
                                        error = False
                                print error

                            #Mensagem de FLW
                            if tipo == 4:
                                print "entrou no tipo FLW"
                                if sock in SOCKET_LIST:
                                    mtd_svr.ok(sock,server_id,id_remet)
                                    mtd_svr.fecharSocket(sock,SOCKET_LIST)



                    except:
                        continue

serversocket.close()
