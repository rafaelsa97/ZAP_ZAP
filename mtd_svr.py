# -*- coding: utf-8 -*-

# =========================== ZAP ZAP - Servidor ============================
# Programa de chat desenvolvido para disciplina de Redes de Computadores
# UNIVERSIDADE FEDERAL DE MINAS GERAIS
# Desenvolvido por Bhryan Henderson Lopes Perpétuo e Rafael Santos de Almeida
# Novembro de 2017
# ===========================================================================

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


def recebe_mensagem(data,sock): #Função que desempacota os dados e retorna-os
	msg = ''
	tipo,id_remet,id_dest,ordem = struct.unpack("!4H",data) #Desempacota o cabeçalho
	if tipo == 5:	#Se for do tipo 5 ele desempacota a mensagem
		tam = struct.unpack("!H",sock.recv(2))
		# Obtém o payload da mensagem
		for i in range(tam[0]):
			byte = struct.unpack('!B',sock.recv(1))
			msg = msg + str(chr(byte[0]))
		return tipo,id_remet,id_dest,ordem,tam[0],msg
	else: # Senão, é dos outros tipos
		return tipo,id_remet,id_dest,ordem,0,0

def ok(s,idf_r,idf_d,ordem): #Função que manda mensagem de OK
	s.send(struct.pack('!4H',1,idf_r,idf_d,ordem))

def erro(s,idf_r,idf_d,ordem): #Função que manda mensagem de ERROR
	s.send(struct.pack('!4H',2,idf_r,idf_d,ordem))

def clist(sock,server_id,id_remet,list,serversocket): #Função que devolve o CLIST para o Cliente
	id = 7
	num = 0
	new_list = ""
	for i in list:
		#Adiciona em uma lista os IDs dos clientes conectados
		if i != 0 and i != serversocket and i != sock:
			id_sock = buscaID(list,i)
			num = num + 1
			new_list = new_list + struct.pack('!H',id_sock)
	#Cria cabeçalho
	aux = struct.pack("!5H",id,server_id,id_remet,0,num)
	#Manda cabeçalho mais a lista com os IDs
	sock.send(aux + new_list)
	#Espera o OK
	ok = sock.recv(8)

def buscaID(list,sock): #Função que busca o ID em que o socket se encontra na lista
    cont = 1 #Começa com contador 1 (0 é o server)
    while cont < len(list):
        if list[cont] == sock: #Se o socket estiver nessa posição da lista retorna a posição
                return cont
        else:	#Se não, ele incrementa o contador
                cont = cont +1

def encaminha_msg(dest,pacote,list): #Encaminha mensagem para o o destinatario
	dest.send(pacote)
	try:
		dest.settimeout(5.0)	#Se o cliente não voltar com o OK em 5s, o destinatário não existe
		ok = dest.recv(8)
	except socket.timeout:
		fecharSocket(dest,list) #Fecha o socket do destinatário

def procuraSock(dest,list): #Função que procura o socket de acordo com o ID dado
        if dest != 65535 and dest < len(list):
        	client = list[dest]
        	if client != 0:
        		return client
        	else:
        		return False
        else:
        	return False

def fecharSocket(sock,list): #Função que fecha o Socket
	try:
		id = buscaID(list,sock)
		sock.close()
		list[id] = 0
	except:
		pass

	print "Cliente (%s) fechado" % str(id)


def encaminha_msg_broadcast (list,msg, sock,server_socket):
    for socket in list:
    	#O socket à ser enviado não pode ser o servidor, nem o próprio socket, e nem sockets já desconectados
        if socket != server_socket and socket != sock and socket != 0 :
            try:
                socket.send(msg) #Tenta enviar a mensagem
            except :
                if socket in list:#se o socket esta na lista de sockets observados pelo select
                    fecharSocket(socket,list) #remove da lista e fecha o socket
