import time
import random
from config import serverName, serverPort
import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_message(distance, angle):
    message = str(distance)+"@"+str(angle)
    message = message.encode('utf-8')
    print(message)
    clientSocket.sendto(message, (serverName, serverPort))


num = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80,
       80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50, 50, 50, 50, 50, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70]
num_inverse = num

try:
    while True:
        for angle in range(0, 180):
            dist = num[angle]
            send_message(dist, angle)
            time.sleep(0.01)

        send_message(-2, -2)

        for angle in range(179, 0, -1):
            dist = num_inverse[180 - angle]
            send_message(dist, angle)
            time.sleep(0.01)

        send_message(-1, -1)
        # LASER
        send_message(20, 100)
        time.sleep(5)
        send_message(-3, -3)

except KeyboardInterrupt:
    print("Stop")
finally:
    clientSocket.close()
