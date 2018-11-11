import socket
import time
from random import *
import array

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 12000


clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

timeSleep = 0.04
maxRange = 180
minRange = 0

angle = 0
status = 0

num = [30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,30,29,28,27,26,25,24,23,22,21,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,50,50,50,50,50,70,70,70,70,70,70,70,70,70,70,70,70,70,70]

while True:

    #num = randint(1, 50)
    # Right 0 -> 180
    if status == 0:
        angle += 1
            
        if angle >= maxRange:
            status = 1
               
    # Left 180 -> 0
    else :
        
        angle -= 1
            
        if angle <= minRange:
            status=0
        #time.sleep(timeSleep)
    
        
    Message = str(num[angle-1])+"@"+str(angle)
        
    clientSock.sendto(Message.encode('utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
    time.sleep(timeSleep)
