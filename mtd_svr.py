import struct

def erro(s,idf_r,idf_d):
	s.send(struct.pack('!4H',2,idf_r,idf_d,69))

def ok(s,idf_r,idf_d):
	s.send(struct.pack('!4H',1,idf_r,idf_d,69))
	print "ok"

def clist(sock,server_id,id_remet,list):
	id = 7
	num = 0
	print "Chegou aqui"
	new_list = ""
	for i in list:
		if i != 0:
			id_sock = buscaID(list,i)
			print "ID SOCKET: " + str(id_sock)
			num = num + 1
			new_list = new_list + struct.pack('!H',id_sock)
	print "Passou"
	aux = struct.pack("!5H",id,server_id,id_remet,0,num)
	sock.send(aux + new_list)

	
def send_message(id_remet,id_dest,data,lista_socket):
	if id_dest == 0:
		for i in lista_socket:
			i.send(data)
			ok(remet,65535,id_remet)
			return True
		
	else:
		dest =  procuraSock(id_dest,lista_socket)
		print "Socket destino: " + str(dest)
		if dest:
			dest.send(data)
			ok(remet,65535,id_remet)
			return True
		else:
			return False


def procuraSock(dest,list):
        if dest != 65535:
                try:
                        client = list[dest]
                        return client
                except:
                        return False
        else:
                return client

def buscaID(list,sock): 
    cont = 0
    while cont < len(list):
        if list[cont] == sock :
                return cont
        else:
                cont +=1

def fecharSocket(sock,list):
    ID = buscaID(sock)
    list[ID] = 0
    sock.close()
