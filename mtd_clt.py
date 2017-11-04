import struct

# msg_OI(socket ligado ao servidor)
# Envia mensagem ao servidor requisitando numero de identificador
# Saida: 0 caso haja falha, 1 caso tenha sucesso
def msg_OI(s):
    s.send(struct.pack('!4H',3,0,1,0))
    idf = s.recv(8)
    # Confere se mensagem de resposta foi recebida
    if not idf:
        print "O programa nao pode obter o numero identificador com o servidor."
        return 0
    s_aux = struct.unpack('!4H',idf)
    idf =  int(s_aux[1])
    # Confere se recebeu um ok do servidor
    print s_aux[0]
    if s_aux[0] == 1:
        print "Identificador: " + str(idf)
        return idf
    else:
        print "Falha na atribuicao de numero de identificador pelo servidor"
        return 0

# msg_MSG(string com a mensagem digitada, numero do identificador, socket de com. com o serv.)
# Insere cabecalho e envia mensagem digitada pelo user para o servidor
# Saida: 0 caso haja falha, 1 caso tenha sucesso
def msg_MSG(msg, idf,s):
    # Cria cabecalho
    tipo = 5
    idf_serv = 65535
    tipo_idf = struct.pack('!3H', tipo, idf, idf_serv)
    # Encapsulamento do tamanho da mensagem
    tam = struct.pack('!H',len(msg))
    s_aux = ""
    for i in msg:
        s_aux = s_aux + struct.pack('!B',ord(i))
    s.send(tipo_idf + tam + s_aux)
    ok = struct.unpack('!4H',s.recv(8))
    if ok[1] == '1':
        return 1
    elif ok[1] == '2':
        return 0

# msg_FLW(identificador do cliente, socket ligado ao servidor)
# Envia mensagem ao servidor informando saida
# Saida: 0 caso haja falha, 1 caso tenha sucesso
def msg_FLW(idf,s):
    # Cria cabecalho
    tipo = 4
    idf_serv = 65535
    tipo_idf = struct.pack('!4H', tipo, idf, idf_serv,69)
    s.send(tipo_idf)
    ok = struct.unpack('!4H',s.recv(8))
    if ok[1] == '1':
        return 1
    else:
        return 0
