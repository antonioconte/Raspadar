from target import *
import sys
from socket import *
import pygame
import math
import colors as c
import time
import os


class Display:
    WIDGHT = 1000
    HEIGHT = 620
    CENTER_RADAR_X = 500
    CENTER_RADAR_Y = 600
    DIS_MAX = 51
    SIZE_OBJ = 4
    SIZE_FIRST = 8

    # initializes Pygame
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    radarDisplay = pygame.display.set_mode((WIDGHT, HEIGHT))
    center_radar = (CENTER_RADAR_X, CENTER_RADAR_Y)
    defaultFont = pygame.font.get_default_font()
    fontRenderer = pygame.font.Font(defaultFont, 16)
    bangFont = pygame.font.Font(defaultFont, 20)
    labelFont = pygame.font.SysFont('Comic Sans MS', 16)
    degreeFont = pygame.font.Font(defaultFont, 20)
    titleFont = pygame.font.SysFont('Agency FB', 60)
    subtitleFont = pygame.font.SysFont('Agency FB', 30)

    MAX_RANGE_PX = 450
    MAX_RANGE_CM = 50

    def __init__(self):
        self.radarDisplay.fill(c.black)
        text = self.subtitleFont.render(
            "Waiting data from client ...", 1, c.gray)
        text_x = self.WIDGHT/2 - text.get_rect().width/2
        text_y = self.HEIGHT/2 - text.get_rect().height/2 + 100
        self.radarDisplay.blit(text, (text_x, text_y))
        text = self.titleFont.render("Welcome to Raspadar!", 1, c.gray)
        text_x = self.WIDGHT/2 - text.get_rect().width/2
        text_y = text_y/2 - text.get_rect().height/2 + 100
        self.radarDisplay.blit(text, (text_x, text_y))
        pygame.display.update()

    def draw_diagram(self):
        self.radarDisplay.fill(c.black)
        RANGE_50 = self.get_distance(50)
        RANGE_45 = self.get_distance(45)
        RANGE_40 = self.get_distance(40)
        RANGE_35 = self.get_distance(35)
        RANGE_30 = self.get_distance(30)
        RANGE_25 = self.get_distance(25)
        RANGE_20 = self.get_distance(20)
        RANGE_15 = self.get_distance(15)
        RANGE_10 = self.get_distance(10)
        RANGE_5 = self.get_distance(5)
        radius_circle = [RANGE_10, RANGE_20, RANGE_30, RANGE_40, RANGE_50]

        pygame.draw.circle(self.radarDisplay, c.green,
                           self.center_radar,  RANGE_50, 1)  # 50
        pygame.draw.circle(self.radarDisplay, c.darkgreen,
                           self.center_radar,  RANGE_45, 1)
        pygame.draw.circle(self.radarDisplay, c.green,
                           self.center_radar,  RANGE_40, 1)  # 40
        pygame.draw.circle(self.radarDisplay, c.darkgreen,
                           self.center_radar,  RANGE_35, 1)
        pygame.draw.circle(self.radarDisplay, c.green,
                           self.center_radar,  RANGE_30, 1)  # 30
        pygame.draw.circle(self.radarDisplay, c.darkgreen,
                           self.center_radar,  RANGE_25, 1)
        pygame.draw.circle(self.radarDisplay, c.green,
                           self.center_radar,  RANGE_20, 1)  # 20
        pygame.draw.circle(self.radarDisplay, c.darkgreen,
                           self.center_radar,  RANGE_15, 1)
        pygame.draw.circle(self.radarDisplay, c.green,
                           self.center_radar,  RANGE_10, 1)  # 10
        pygame.draw.circle(self.radarDisplay, c.darkgreen,
                           self.center_radar,  RANGE_5, 1)

        # draw under radar
        self.radarDisplay.fill(
            c.black, [0, self.CENTER_RADAR_Y+1, self.WIDGHT, 19])

        # horizental line
        HL_start = 20
        HL_end = self.WIDGHT - 20
        CENTER = self.WIDGHT / 2
        pygame.draw.line(self.radarDisplay, c.green, (HL_start, self.CENTER_RADAR_Y),
                         (HL_end, self.CENTER_RADAR_Y), 2)

        # x,y = raggio * cos(45))
        # 45 degree line
        # 45 degree line
        X_45 = CENTER - 339
        Y_45 = CENTER - 339

        # 135 degree line
        X_135 = CENTER + 339
        Y_135 = CENTER - 339

        # 45 degree line
        pygame.draw.line(self.radarDisplay, colors.green,
                         (500, 600), (154, 255), 1)
        # 90 degree line
        pygame.draw.line(self.radarDisplay, colors.green,
                         (500, 600), (500, 105), 1)
        # 135 degree line
        pygame.draw.line(self.radarDisplay, colors.green,
                         (500, 600), (845, 255), 1)

        # draw stastics board
        pygame.draw.rect(self.radarDisplay, colors.blue, [20, 10, 270, 90], 2)

        # write the 0 degree
        text = self.degreeFont.render("0", 1, colors.forestgreen)
        self.radarDisplay.blit(text, (20, 570))

        # write the 45 degree
        text = self.degreeFont.render("45", 1, colors.forestgreen)
        self.radarDisplay.blit(text, (135, 230))

        # write the 90 degree
        text = self.degreeFont.render("90", 1, colors.forestgreen)
        self.radarDisplay.blit(text, (490, 80))

        # write the 135 degree
        text = self.degreeFont.render("135", 1, colors.forestgreen)
        self.radarDisplay.blit(text, (845, 230))

        # write the 180 degree
        text = self.degreeFont.render("180", 1, colors.forestgreen)
        self.radarDisplay.blit(text, (955, 570))

        # write distance
        labels = ["10 cm", "20 cm", "30 cm", "40 cm", "50 cm"]
        for i in range(5):
            text = self.labelFont.render(labels[i], 1, c.gray)
            text_x = CENTER - (text.get_rect().width)/2
            text_y = CENTER - radius_circle[i] + 80
            self.radarDisplay.blit(text, (text_x, text_y))

    def print_informations(self, distance, angle):
        # write angle
        message = "Angle : " + str(angle)
        text = self.fontRenderer.render(message, 1, c.white)
        self.radarDisplay.blit(text, (40, 30))
        # write distance
        if distance >= self.DIS_MAX:
            message = "Distance : Out of Range"
        else:
            message = "Distance : " + str(distance) + " cm"
        text = self.fontRenderer.render(message, 1, c.white)
        self.radarDisplay.blit(text, (40, 60))
        # write title
        title = self.titleFont.render("Raspadar", 1, c.white)
        self.radarDisplay.blit(title, (700, 60))

    def get_distance(self, distance):
        x = int(self.MAX_RANGE_PX * distance / self.MAX_RANGE_CM)
        return x

    def draw_line(self, angle):
        # line_radar blue
        radius = float(self.MAX_RANGE_PX)
        r_x = math.cos(math.radians(angle)) * radius
        r_y = math.sin(math.radians(angle)) * radius
        pygame.draw.line(self.radarDisplay, c.blue, self.center_radar,
                         (self.CENTER_RADAR_X-int(r_x), self.CENTER_RADAR_Y-int(r_y)), 3)

    def get_position_element(self, distance, angle):
        obj_x = math.cos(math.radians(angle)) * self.get_distance(distance)
        obj_y = math.sin(math.radians(angle)) * self.get_distance(distance)
        position = (self.CENTER_RADAR_X - int(obj_x),
                    self.CENTER_RADAR_Y - int(obj_y))
        return position

    def draw_single_element(self, distance, angle, info):
        # object
        position = self.get_position_element(distance, angle)
        if info == 0:
            color = c.yellow
        elif info == 1:
            color = c.orange
            text = self.bangFont.render("Bang", 1, c.red)
            self.radarDisplay.blit(text, (40, 100))

        pygame.draw.circle(self.radarDisplay, color, position, self.SIZE_FIRST)
        # pygame.display.update()

    def drawing_target(self, targets):
        for angle in list(targets):
            position = position = self.get_position_element(
                targets[angle].distance, targets[angle].angle)
            pygame.draw.circle(self.radarDisplay,
                               targets[angle].color, position, self.SIZE_OBJ)

    def drawing(self, distance, angle, targets, targets_precedente, iterazione):
        self.draw_diagram()
        if distance > 0:
            self.print_informations(distance, angle)

        if iterazione == 1:
            self.drawing_target(targets)
        if iterazione == 2:
            self.drawing_target(targets_precedente)
            self.drawing_target(targets)
        if iterazione == 3:
            self.draw_single_element(distance, angle, 1)

        if (distance >= 2.0) and (distance <= 51.0) and iterazione != 3:
            self.draw_single_element(distance, angle, 0)

        self.draw_line(angle)
        pygame.display.update()

    def stop(self):
        print("STOP")
        time.sleep(2)
        pygame.quit()


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print("Server is ready.")
display = Display()

targets = dict()
previous_targets = dict()
iterazione = 1


def draw_point(distance, angle, passata):
    global targets
    global previous_targets
    global iterazione

    if distance == -2:
        # cmabio il colore a Target
        for angle in list(targets):
            targets[angle].color = colors.red6L
        display.drawing_target(targets)
        previous_targets = targets.copy()
        targets.clear()
        iterazione = 2
        return None
    elif distance == -1:
        # pulisco Targets
        targets.clear()
        previous_targets.clear()
        iterazione = 3
    elif distance == -3:
        targets.clear()
        previous_targets.clear()
        iterazione = 1
    elif (distance > -1) and (distance <= 50):
        targets[angle] = Target(angle, distance)

    if distance > 0:
        display.drawing(distance, angle, targets, previous_targets, iterazione)


try:
    while True:
        message = serverSocket.recv(2048)
        message = str(message.decode())
        distance, angle = message.split('@')
        distance = float(distance)
        angle = float(angle)
        draw_point(distance, angle, iterazione)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Exception('Quit')
except (KeyboardInterrupt, Exception) as e:
    print(repr(e))
finally:
    display.stop()
