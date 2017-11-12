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


def server():
    n = 0
    mtd_svr.apresentacao()

    #Criacao do socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Aportando no porto do IP indicado
    serversocket.bind((IP, PORTO))
    #Esperando por conexao
    serversocket.listen(255)
    #Colocar na lista de sockets, o socket do servidor
    SOCKET_LIST.insert(n,serversocket)
    n = n + 1

    print "Chat server iniciado no porto: " + str(PORTO)

    # Envia identificador para o cliente
    while 1:

        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:

                    if sock == serversocket:
                            client,addr = serversocket.accept()
                            SOCKET_LIST.insert(n,client)
                            n = n + 1
                            data = client.recv(8) # Recebe requisicao inicial do cliente para conectar ao servidor
                            if not data:
                                print "ERRO\nNão foi possível o cliente conectar ao servidor"
                                serversocket.close()
                                sys.exit(0)
                            else:
                                print "Cliente (%s, %s) connectado" % addr
                                data = struct.unpack('!4H',data)
                                if data[0] == 3: # Identifica se recebeu um pacote tipo OI
                                        new_client_id = mtd_svr.buscaID(SOCKET_LIST,client)
                                        if not new_client_id:
                                                print "Não foi possível atribuir núm.de identificadorao cliente"
                                                break
                                        else:
                                                mtd_svr.ok(client,server_id,new_client_id,0)

                    else:
                              # process data recieved from client,
                        try:
                            # receiving data from the socket.
                            data = sock.recv(8)
                        except:
                            mtd_svr.fecharSocket(sock,SOCKET_LIST)
                            continue
                        if data:
                            if data:
                                tipo,id_remet,id_dest,ordem,tam,msg = mtd_svr.recebe_mensagem(data,sock)
                                socketID = mtd_svr.procuraSock(id_remet,SOCKET_LIST)
                                if socketID != sock:
                                    print "Socket falso"
                                    mtd_svr.erro(socket,server_id,id_remet,ordem)
                                    break    

                                #Mensagem de CREQ
                                if tipo == 6:
                                    mtd_svr.clist(sock,server_id,id_remet,SOCKET_LIST,serversocket)

                                #Mensagem para outro
                                if tipo == 5:
                                    s_aux = ""
                                    # Empacota o payload
                                    for c in msg:
                                        s_aux = s_aux + struct.pack('!B',ord(c))
                                    #Reconstroi o pacote
                                    tam = struct.pack('!H',tam)
                                    pacote = data + tam + s_aux
                                    if id_dest == 0: #Broadcast
                                        mtd_svr.ok(sock,server_id,id_remet,ordem)                                  
                                        mtd_svr.encaminha_msg_broadcast(SOCKET_LIST,pacote,sock,serversocket) # Encaminha mensagem aos clientes
                                    else: # Mensagem para cliente específico
                                        dest =  mtd_svr.procuraSock(id_dest,SOCKET_LIST)
                                        if dest != 0:
                                            mtd_svr.ok(sock,server_id,id_remet,ordem)
                                            mtd_svr.encaminha_msg(dest,pacote,SOCKET_LIST)
                                        else:
                                            mtd_svr.erro(sock,server_id,id_remet,ordem)

                                #Mensagem de FLW
                                if tipo == 4:
                                    if sock in SOCKET_LIST:
                                        mtd_svr.ok(sock,server_id,id_remet,ordem)
                                        mtd_svr.fecharSocket(sock,SOCKET_LIST)

    serversocket.close()

if __name__ == "__main__": #inicio do programa

    sys.exit(server()) #chama a funcao e sai