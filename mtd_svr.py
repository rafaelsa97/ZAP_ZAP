import struct

def erro(s,idf_r,idf_d):
	s.send(struct.pack('!4H',2,idf_r,idf_d,69))

def ok(s,idf_r,idf_d):
	s.send(struct.pack('!4H',1,idf_r,idf_d,69))