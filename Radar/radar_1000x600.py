import pygame
import math
import time
import colors
import sys
from target import *
from display import draw
import socket
#import os

###### Socket setting
UDP_IP_ADDRESS = ""
UDP_PORT_NO = 12000

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

# initialize the program
#os.environ['SDL_VIDEO_CENTERED'] = '1'
x = pygame.init()

pygame.font.init()

defaultFont = pygame.font.get_default_font()

fontRenderer = pygame.font.Font(defaultFont, 20)

radarDisplay = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)

pygame.display.set_caption('Raspadar')

maxRange = 180
minRange = 0

angle = 0.0
status = 0


# targets list
targets = {}

try:
    
    while True:

        data, addr = serverSock.recvfrom(256)
        

        Message = str(data.decode())
        dist, ang = Message.split("@")

        distance = float (dist)
        oppositeAngle = float(ang)
        angle = 180-oppositeAngle
        if distance == -1 and oppositeAngle == -1:
            targets.clear()
        # change the condition if the range is changed
        elif distance != -1 and distance <= 50:
            targets[angle] = Target(angle, distance)

        draw(radarDisplay, targets, angle, distance, fontRenderer)
        # detect if close is pressed to stop the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #set servomotore a 0 gradi
                raise KeyboardInterrupt
        
    
except KeyboardInterrupt:
    print('Radar Exit --> KeyboardInterrupt')

except Exception as e:
    print("Exception: ", e)
    print('Radar Exit--> Exception')

pygame.quit()
sys.exit()