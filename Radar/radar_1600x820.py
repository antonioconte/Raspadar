from target import *
import sys
from socket import *
import pygame
import math
import colors as c
import time
import os


class Display:
    WIDGHT = 1600
    HEIGHT = 820
    CENTER_RADAR_X = 800
    CENTER_RADAR_Y = 800
    DIS_MAX = 51
    SIZE_OBJ = 10
    SIZE_FIRST = 15

    # initializes Pygame
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    radarDisplay = pygame.display.set_mode((WIDGHT, HEIGHT))
    center_radar = (CENTER_RADAR_X, CENTER_RADAR_Y)
    defaultFont = pygame.font.get_default_font()
    fontRenderer = pygame.font.Font(defaultFont, 16)
    labelFont = pygame.font.SysFont('Comic Sans MS', 16)
    titleFont = pygame.font.SysFont('Agency FB', 60)
    subtitleFont = pygame.font.SysFont('Agency FB', 30)

    MAX_RANGE_PX = 700
    MAX_RANGE_CM = 50

    def __init__(self):
        self.radarDisplay.fill(c.black)
        text = self.subtitleFont.render(
            "Waiting data from client ...", 1, c.gray)
        text_x = self.WIDGHT/2 - text.get_rect().width/2
        text_y = self.HEIGHT/2 - text.get_rect().height/2
        self.radarDisplay.blit(text, (text_x, text_y))
        text = self.titleFont.render("Welcome to Raspadar!", 1, c.gray)
        text_x = self.WIDGHT/2 - text.get_rect().width/2
        text_y = text_y/2 - text.get_rect().height/2
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
        HL_start = 70
        HL_end = self.WIDGHT - 70
        CENTER = self.WIDGHT / 2
        pygame.draw.line(self.radarDisplay, c.green, (HL_start, self.CENTER_RADAR_Y),
                         (HL_end, self.CENTER_RADAR_Y), 2)

        # x,y = raggio * cos(45))
        # 730 * cos(45) = 516
        # 45 degree line
        X_45 = CENTER - 516
        Y_45 = CENTER - 516
        pygame.draw.line(self.radarDisplay, c.green,
                         self.center_radar, (X_45, Y_45), 1)
        # 90 degree line
        pygame.draw.line(self.radarDisplay, c.green,
                         self.center_radar, (CENTER, HL_start), 1)
        # 135 degree line
        X_135 = CENTER + 516
        Y_135 = CENTER - 516
        pygame.draw.line(self.radarDisplay, c.green,
                         self.center_radar, (X_135, Y_135), 1)

        # write distance
        labels = ["10 cm", "20 cm", "30 cm", "40 cm", "50 cm"]
        for i in range(5):
            text = self.labelFont.render(labels[i], 1, c.gray)
            text_x = CENTER - (text.get_rect().width)/2
            text_y = CENTER - radius_circle[i] - 20
            self.radarDisplay.blit(text, (text_x, text_y))

        # write degree
        labels = ["0", "45", "90", "135", "180"]
        label_x = [(HL_start-1), (X_45-10), (CENTER), (X_135+10), (HL_end - 1)]
        label_y = [(CENTER-10), (Y_45-10), (HL_start-10),
                   (Y_135-10), (CENTER - 10)]
        for i in range(5):
            text = self.fontRenderer.render(labels[i], 1, c.darkgreen)
            text_x = label_x[i] - (text.get_rect().width)/2
            text_y = label_y[i] - (text.get_rect().height)/2
            self.radarDisplay.blit(text, (text_x, text_y))

    def print_informations(self, distance, angle):
        # write angle
        message = "Angle : " + str(angle)
        text = self.fontRenderer.render(message, 1, c.white)
        self.radarDisplay.blit(text, (40, 25))
        # write distance
        if distance >= self.DIS_MAX:
            message = "Distance : Out of Range"
        else:
            message = "Distance : " + str(distance) + " cm"
        text = self.fontRenderer.render(message, 1, c.white)
        self.radarDisplay.blit(text, (40, 60))
        # write title
        title = self.titleFont.render("Raspadar", 1, c.white)
        self.radarDisplay.blit(title, (1300, 60))
        # draw stastics board
        pygame.draw.rect(self.radarDisplay, colors.blue, [20, 10, 225, 80], 2)

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
        # la testa sarebbe l'elemento rilevato in quell'istante
        position = self.get_position_element(distance, angle)
        if info == 0:
            color = c.yellow
        elif info == 1:
            color = c.orange
        pygame.draw.circle(self.radarDisplay, color, position, self.SIZE_FIRST)

    def drawing_target(self, targets):
        print(targets.keys)
        print(targets.values)
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
            time.sleep(1)
            self.drawing_target(targets)
        if iterazione == 3:
            self.draw_single_element(distance, angle, 1)

        if (distance >= 2.0) and (distance <= 51.0) and iterazione != 3:
            self.draw_single_element(distance, angle, 0)

        self.draw_line(angle)
        pygame.display.update()

    def stop_radar(self):
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


def draw_point(distance, angle):
    global targets
    global previous_targets
    global iterazione

    if distance == -2:
        # cmabio il colore a Target
        for angle in list(targets):
            targets[angle].color = colors.red6L
        display.drawing_target(targets)
        previous_targets = targets
        iterazione = 2
        return None
    elif distance == -1:
        # pulisco Targets
        targets.clear()
        previous_targets.clear()
        iterazione = 3
    elif (distance > -1) and (distance <= 50):
        targets[angle] = Target(angle, distance)

    display.drawing(distance, angle, targets, previous_targets, iterazione)


try:
    while True:
        message = serverSocket.recv(2048)
        message = str(message.decode())
        distance, angle = message.split('@')
        distance = float(distance)
        angle = float(angle)
        draw_point(distance, angle)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Exception('Quit')
except (KeyboardInterrupt, Exception) as e:
    print(repr(e))
finally:
    display.stop_radar()
