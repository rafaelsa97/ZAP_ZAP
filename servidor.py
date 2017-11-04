#TP0 REDES - RAFAEL SANTOS DE ALMEIDA - 2015123614
#ENGENHARIA DE CONTROLE E AUTOMACAO - UFMG

import socket
import struct
import time

#Endereco IP e porto da comunicacao
IP = ''
PORTO = 51513

#Criacao do socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Aportando no porto do IP indicado
serversocket.bind((IP, PORTO))
#Esperando por conexao
serversocket.listen(1)

# Envia identificador para o cliente
while 1:
	#Aceita a conexao
	(client, addr) = serversocket.accept()
	# Recebe requisicao do cliente
	data = client.recv(8)
	if not data:
		break
	else:
		data = struct.unpack('!4H',data)
		print data[0]
		client.send(struct.pack('!4H',1,8,1,8))

	# Recebe mensagens do cliente
	while 1:
		tipo = client.recv(2)
		idf1 = client.recv(2)
		idf2 = client.recv(2)
		tam  = struct.unpack(client.recv(2))
		#tam = struct.unpack('!c')

		s_aux = struct.unpack('!s', data)
		if not data:
			print "Deu ruim"
			break

		if s_aux[1] == '4':
			print "Desconectou"
			client.send(struct.pack('!i',1818))
			break
		else:
			print data
			client.send(struct.pack('!i',1818))
	client.close
