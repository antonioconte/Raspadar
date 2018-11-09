import socket as s

addr = "192.168.43.117"
port = 12000
print(">SERVER")
server =  s.socket(s.AF_INET, s.SOCK_DGRAM)
server.bind((addr, port))

while True:
    data, a = server.recvfrom(1024)
    print(data)
