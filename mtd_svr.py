# -*- coding: utf-8 -*-
import struct
import socket
import time

class bcolors:
    HEADER = '\033[95m'  # Rosa claro
    OKBLUE = '\033[94m'  # Azul
    OKGREEN = '\033[92m' # Verde
    WARNING = '\033[93m' # Amarelo
    FAIL = '\033[91m'    # Vermelho
    ENDC = '\033[0m'     # Branco

def apresentacao():
    print bcolors.OKBLUE + "\n\n███████╗ █████╗ ██████╗     ███████╗ █████╗ ██████╗ " + bcolors.ENDC
    print bcolors.OKBLUE + "╚══███╔╝██╔══██╗██╔══██╗    ╚══███╔╝██╔══██╗██╔══██╗" + bcolors.ENDC
    print bcolors.OKBLUE + "  ███╔╝ ███████║██████╔╝      ███╔╝ ███████║██████╔╝" + bcolors.ENDC
    print bcolors.OKBLUE + " ███╔╝  ██╔══██║██╔═══╝      ███╔╝  ██╔══██║██╔═══╝ " + bcolors.ENDC
    print bcolors.OKBLUE + "███████╗██║  ██║██║         ███████╗██║  ██║██║     " + bcolors.ENDC
    print bcolors.OKBLUE + "╚══════╝╚═╝  ╚═╝╚═╝         ╚══════╝╚═╝  ╚═╝╚═╝     \n" + bcolors.ENDC
    print bcolors.OKBLUE + "Por Bhryan Henderson e Rafael Santos de Almeida\n" + bcolors.ENDC
def erro(s,idf_r,idf_d,ordem):
	s.send(struct.pack('!4H',2,idf_r,idf_d,ordem))

# recebe_cabecalho(cabeçalho empacotado, socket do cliente)
# Recebe mensagem do cliente
# Saida: dados do pacote desempacotados
def recebe_mensagem(data,sock):
	msg = ''
	tipo,id_remet,id_dest,ordem = struct.unpack("!4H",data)
	if tipo == 5:
		tam = struct.unpack("!H",sock.recv(2))
		# Obtém o payload da mensagem
		for i in range(tam[0]):
			byte = struct.unpack('!B',sock.recv(1))
			msg = msg + str(chr(byte[0]))
		return tipo,id_remet,id_dest,ordem,tam[0],msg
	else:
		return tipo,id_remet,id_dest,ordem,0,0

def ok(s,idf_r,idf_d,ordem):
	s.send(struct.pack('!4H',1,idf_r,idf_d,ordem))

def clist(sock,server_id,id_remet,list,serversocket):
	id = 7
	num = 0
	new_list = ""
	for i in list:
		if i != 0 and i != serversocket and i != sock:
			id_sock = buscaID(list,i)
			num = num + 1
			new_list = new_list + struct.pack('!H',id_sock)
	aux = struct.pack("!5H",id,server_id,id_remet,0,num)
	sock.send(aux + new_list)
	ok = sock.recv(8)

def buscaID(list,sock):
    cont = 1
    while cont < len(list):
        if list[cont] == sock :
                return cont
        else:
                cont = cont +1

def encaminha_msg(dest,pacote,list):
	dest.send(pacote)
	try:
		dest.settimeout(5.0)
		ok = dest.recv(8)
	except socket.timeout:
		fecharSocket(dest,list)

def procuraSock(dest,list):
        if dest != 65535 and dest < len(list):
        	client = list[dest]
        	if client != 0:
        		return client
        	else:
        		return False
        else:
        	return False

def fecharSocket(sock,list):
	id = buscaID(list,sock)
	sock.close()
	list[id] = 0

	print "Cliente (%s) fechado" % str(id)


def encaminha_msg_broadcast (list,msg, sock,server_socket):
    for socket in list:#para todos os sockets na lista de sockets observados pelo select
        if socket != server_socket and socket != sock and socket != 0 :#se o socket nao e o servidor nem quem esta fazendo o broadcast
            try:
                socket.send(msg) #tenta enviar a msg
            except :#se algo der errado, socket corrompido
                if socket in list:#se o socket esta na lista de sockets observados pelo select
                    fecharSocket(socket,list) #remove da lista
