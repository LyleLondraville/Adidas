import socket, ast

s = socket.socket()

s.bind(('', 8080))
s.listen(1)


conn, addr = s.accept()

d = conn.recv(10000000)
d = ast.literal_eval(d)

##insert cookies into browser from here and open selenium

