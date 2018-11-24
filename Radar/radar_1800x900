import pygame
import math
import colors as c
import time
import os


class Display:
    WIDGHT = 1800
    HEIGHT = 920
    CENTER_RADAR_X = 900
    CENTER_RADAR_Y = 900
    DIS_MAX = 51
    SIZE_OBJ = 10

    # initializes Pygame
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    radarDisplay = pygame.display.set_mode((WIDGHT, HEIGHT))

    center_radar = (CENTER_RADAR_X, CENTER_RADAR_Y)
    defaultFont = pygame.font.get_default_font()
    fontRenderer = pygame.font.Font(defaultFont, 16)
    labelFont = pygame.font.SysFont('Comic Sans MS', 16)
    titleFont = pygame.font.SysFont('Agency FB', 60)

    def __init__(self):
        self.radarDisplay.fill(c.black)
        text = self.titleFont.render("Welcome to Raspadar!", 1, c.gray)
        text_x = self.WIDGHT/2 - text.get_rect().width/2
        text_y = self.HEIGHT/2 - text.get_rect().height/2
        self.radarDisplay.blit(text, (text_x, text_y))
        pygame.display.update()

    def draw_diagram(self):
        MAX_RANGE_PX = 800
        MAX_RANGE_CM = 50
        self.radarDisplay.fill(c.black)
        pygame.draw.circle(self.radarDisplay, c.green,
                           self.center_radar,  int(MAX_RANGE_PX*50/MAX_RANGE_CM), 1)  # 50
        pygame.draw.circle(self.radarDisplay, c.darkgreen,
                           self.center_radar,  int(MAX_RANGE_PX*45/MAX_RANGE_CM), 1)
        pygame.draw.circle(self.radarDisplay, c.green,
                           self.center_radar,  int(MAX_RANGE_PX*40/MAX_RANGE_CM), 1)  # 40
        pygame.draw.circle(self.radarDisplay, c.darkgreen,
                           self.center_radar,  int(MAX_RANGE_PX*35/MAX_RANGE_CM), 1)
        pygame.draw.circle(self.radarDisplay, c.green,
                           self.center_radar,  int(MAX_RANGE_PX*30/MAX_RANGE_CM), 1)  # 30
        pygame.draw.circle(self.radarDisplay, c.darkgreen,
                           self.center_radar,  int(MAX_RANGE_PX*25/MAX_RANGE_CM), 1)
        pygame.draw.circle(self.radarDisplay, c.green,
                           self.center_radar,  int(MAX_RANGE_PX*20/MAX_RANGE_CM), 1)  # 20
        pygame.draw.circle(self.radarDisplay, c.darkgreen,
                           self.center_radar,  int(MAX_RANGE_PX*15/MAX_RANGE_CM), 1)
        pygame.draw.circle(self.radarDisplay, c.green,
                           self.center_radar,  int(MAX_RANGE_PX*10/MAX_RANGE_CM), 1)  # 10
        pygame.draw.circle(self.radarDisplay, c.darkgreen,
                           self.center_radar,  int(MAX_RANGE_PX*5/MAX_RANGE_CM), 1)

        # draw under radar
        self.radarDisplay.fill(
            c.black, [0, self.CENTER_RADAR_Y+1, self.WIDGHT, 19])

        # horizental line
        P_70 = 70
        P_1730 = 1730
        P_900 = 900
        pygame.draw.line(self.radarDisplay, c.green, (P_70, self.CENTER_RADAR_Y),
                         (P_1730, self.CENTER_RADAR_Y), 2)
        # 45 degree line
        X_45 = self.center_radar[0]-586
        Y_45 = self.center_radar[1]-586
        pygame.draw.line(self.radarDisplay, c.green,
                         self.center_radar, (X_45, Y_45), 1)
        # 90 degree line
        pygame.draw.line(self.radarDisplay, c.green,
                         self.center_radar, (P_900, P_70), 1)
        # 135 degree line
        X_135 = self.center_radar[0]+586
        Y_135 = self.center_radar[1]-586
        pygame.draw.line(self.radarDisplay, c.green,
                         self.center_radar, (X_135, Y_135), 1)

        # write distance
        center_text_x = 900
        center_text_y = 900
        distance_y = 160
        labels = ["10 cm", "20 cm", "30 cm", "40 cm", "50 cm"]
        for i in range(5):
            text = self.labelFont.render(labels[i], 1, c.gray)
            text_x = center_text_x - (text.get_rect().width)/2
            text_y = center_text_y - distance_y * \
                (i+1) - (text.get_rect().height) + 4
            self.radarDisplay.blit(text, (text_x, text_y))

        # write degree
        labels = ["-90", "-45", "0", "+45", "+90"]
        label_x = [(P_70-1), (X_45-10), (P_900), (X_135+10), (P_1730 - 1)]
        label_y = [(P_900-10), (Y_45-10), (P_70-10), (Y_135-10), (P_900 - 10)]
        for i in range(5):
            text = self.fontRenderer.render(labels[i], 1, c.darkgreen)
            text_x = label_x[i] - (text.get_rect().width)/2
            text_y = label_y[i] - (text.get_rect().height)/2
            self.radarDisplay.blit(text, (text_x, text_y))

    def draw_object(self, distance, angle):
        # object
        obj_x = math.cos(math.radians(angle))*(16)*distance
        obj_y = math.sin(math.radians(angle))*(16)*distance
        position = (self.CENTER_RADAR_X - int(obj_x),
                    self.CENTER_RADAR_Y - int(obj_y))
        pygame.draw.circle(self.radarDisplay, c.red, position, self.SIZE_OBJ)

    def draw_line(self, angle):
        # line_radar blue
        radius = 800.0
        r_x = math.cos(math.radians(angle))*radius
        r_y = math.sin(math.radians(angle))*radius
        pygame.draw.line(self.radarDisplay, c.blue, self.center_radar,
                         (self.CENTER_RADAR_X-int(r_x), self.CENTER_RADAR_Y-int(r_y)), 3)

    def print_informations(self, distance, angle):
        # write angle
        message = "Angle : " + str(angle)
        text = self.fontRenderer.render(message, 1, c.white)
        self.radarDisplay.blit(text, (40, 20))
        # write distance
        if distance == self.DIS_MAX or distance == -1:
            message = "Distance : Out of Range"
        else:
            message = "Distance : " + str(distance) + " cm"
        text = self.fontRenderer.render(message, 1, c.white)
        self.radarDisplay.blit(text, (40, 50))
        # write title
        title = self.titleFont.render("Raspadar", 1, c.white)
        self.radarDisplay.blit(title, (1400, 60))

    def drawing_target(self, targets):

        for angle in list(targets):
            target_x = math.cos(math.radians(
                targets[angle].angle))*(16)*targets[angle].distance
            target_y = math.sin(math.radians(
                targets[angle].angle))*(16)*targets[angle].distance
            position = (self.CENTER_RADAR_X - int(target_x),
                        self.CENTER_RADAR_Y - int(target_y))
            pygame.draw.circle(self.radarDisplay,
                               targets[angle].color, position, self.SIZE_OBJ)

            diffTime = time.time() - targets[angle].time
            if diffTime >= 0.0 and diffTime <= 0.5:
                targets[angle].color = colors.red1L
            elif diffTime > 0.5 and diffTime <= 1:
                targets[angle].color = colors.red2L
            elif diffTime > 1.0 and diffTime <= 1.5:
                targets[angle].color = colors.red3L
            elif diffTime > 1.5 and diffTime <= 2:
                targets[angle].color = colors.red4L
            elif diffTime > 2 and diffTime <= 2.5:
                targets[angle].color = colors.red5L
            elif diffTime > 2.5 and diffTime <= 3.0:
                targets[angle].color = colors.red6L
            elif diffTime > 3.5:
                del targets[angle]

    def drawing(self, distance, angle, targets):
        self.draw_diagram()
        self.print_informations(distance, angle)
        if (distance != -1.0) and (distance != 51.0):
            self.draw_object(distance, angle)
        self.drawing_target(targets)
        self.draw_line(angle)
        pygame.display.update()

    def stop(self):
        print("STOP")
        time.sleep(5)
        pygame.quit()


from socket import *
import sys
from target import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print("Server is ready.")
display = Display()

# distance = [10, 20, 30, 40, 50, 80]
# angle = [25, 45, 90, 135, 170, 160]

targets = {}
try:
    while True:
        message = serverSocket.recv(2048)
        message = str(message.decode())
        if message == "quit":
            break
        else:
            distance, angle = message.split('@')
        distance = float(distance)
        angle = float(angle)
        if (distance == -1) and (distance == -1):
            targets.clear()
        elif (distance != -1) and (distance <= 50):
            targets[angle] = Target(angle, distance)

        display.drawing(distance, angle, targets)
        print(message)

        # for i in range(6):
        #     distance = distance[i]
        #     angle = angle[i]
        #     distance = float(distance)

        #     angle = float(angle)
        #     if (distance != -1) and (distance <= 50):
        #         targets[angle] = Target(angle, distance)

        #     display.drawing(distance, angle, targets)
        #     print(message)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Exception('Quit')
except (KeyboardInterrupt, Exception) as e:
    print(repr(e))
finally:
    display.stop()
