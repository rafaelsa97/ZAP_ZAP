#TP0 REDES - RAFAEL SANTOS DE ALMEIDA - 2015123614
#ENGENHARIA DE CONTROLE E AUTOMACAO - UFMG

import socket
import struct
import mtd_svr

#Endereco IP e porto da comunicacao
IP = '127.0.0.1'
PORTO = 51515

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
		client.send(struct.pack('!4H',1,8,1,8))

	# Recebe mensagens do cliente
	while 1:
		header = client.recv(8)
		header_unpacked = struct.unpack("!4H",header)
		if(header_unpacked[0] == 4):
			print "Falou cuzao"
			break
		mensagem = ""
		for i in range(header_unpacked[3]):
			a = struct.unpack('!B',client.recv(1))
			mensagem = mensagem + str(chr(a[0]))
		print mensagem

		mtd_svr.ok(client,header_unpacked[1],header_unpacked[2])
	client.send(struct.pack('!4H',1,8,1,8))
	client.close
