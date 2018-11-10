import colors
import pygame
import math
import time

distMax = 50
# This module draws the radar screen

def draw(radarDisplay, targets, angle, distance, fontRenderer):
     # draw initial screen
    radarDisplay.fill(colors.black)
    
    pygame.draw.circle(radarDisplay, colors.green, (500,590), 450, 1)

    pygame.draw.circle(radarDisplay, colors.green, (500,590), 400, 1)

    pygame.draw.circle(radarDisplay, colors.green, (500,590), 350, 1)

    pygame.draw.circle(radarDisplay, colors.green, (500,590), 300, 1)

    pygame.draw.circle(radarDisplay, colors.green, (500,590), 250, 1)

    pygame.draw.circle(radarDisplay, colors.green, (500,590), 200, 1)

    pygame.draw.circle(radarDisplay, colors.green, (500,590), 150, 1)


    radarDisplay.fill(colors.white, [0, 600, 1000, 20])
    #x45 = +500 + 1.41*500/2
    # horizental line
    pygame.draw.line(radarDisplay, colors.green, (10, 590), (990, 590), 3)

    # 45 degree line
    pygame.draw.line(radarDisplay, colors.green, (500, 590),(154, 255), 1)

    # 90 degree line
    pygame.draw.line(radarDisplay, colors.green, (500, 590), (500, 80), 1)

    # 135 degree line
    pygame.draw.line(radarDisplay, colors.green, (500, 590), (845, 255), 1)

    # draw stastics board
    pygame.draw.rect(radarDisplay, colors.blue, [20, 20, 270, 100], 2)

    # write the 0 degree
    text = fontRenderer.render("0", 1, colors.green)
    radarDisplay.blit(text,(20,560))

    # write the 45 degree
    text = fontRenderer.render("45", 1, colors.green)
    radarDisplay.blit(text,(135,230))

    # write the 90 degree
    text = fontRenderer.render("90", 1, colors.green)
    radarDisplay.blit(text,(490,60))

    # write the 135 degree
    text = fontRenderer.render("135", 1, colors.green)
    radarDisplay.blit(text,(845, 230))

    # write the 180 degree
    text = fontRenderer.render("180", 1, colors.green)
    radarDisplay.blit(text,(960,560))

    # draw the moving line
    a = math.sin(math.radians(angle)) * 480.0
    b = math.cos(math.radians(angle)) * 480.0
    pygame.draw.line(radarDisplay, colors.blue, (500,590), (500 - int(b), 590 - int(a)), 3)


    # write the current angle
    text = fontRenderer.render("Angle : " + str(angle), 1, colors.white)
    radarDisplay.blit(text,(40,40))

    # write the distance
    #if distance < -1:
    #    text = fontRenderer.render("Distance : Client Stopped" , 1, colors.white)
    if distance == -1 or distance > distMax:
        text = fontRenderer.render("Distance : Out Of Range" , 1, colors.white)
    else: 
        text = fontRenderer.render("Distance : " + str(distance) + " cm" , 1, colors.white)

    radarDisplay.blit(text,(40,80))

    # write the distance
    
    title = fontRenderer.render("Ultrasonic Radar" , 1, colors.white)

    radarDisplay.blit(title,(700,60))

    # draw targets
    for angle in list(targets):
    
        # calculate the coordinates and the remoteness of the target
        c = math.sin(math.radians(targets[angle].angle)) * 450.0
        d = math.cos(math.radians(targets[angle].angle)) * 450.0
	    # change the scale if the range is changed
        e = math.sin(math.radians(targets[angle].angle)) * (450 / distMax) * targets[angle].distance
        f = math.cos(math.radians(targets[angle].angle)) * (450 / distMax) * targets[angle].distance

        #Draw Rectangle
        rectangle = pygame.Rect(490 - int(f), 580 - int(e), 10,10)
        pygame.draw.rect(radarDisplay, targets[angle].color, rectangle)

        #Draw Circle
        #pygame.draw.circle(radarDisplay, targets[angle].color,(500 - int(f), 590 - int(e)) , 7)

        #Draw Line
        #pygame.draw.line(radarDisplay, targets[angle].color, (500 - int(f), 590 - int(e)), (500 - int(d), 590 - int(c)), 3)


        # fading
        diffTime = time.time() - targets[angle].time
        
        if diffTime >= 0.0 and diffTime <= 0.5:
            targets[angle].color = colors.red1L
        elif diffTime > 0.5 and diffTime <= 1:
            targets[angle].color = colors.red2L
        elif diffTime > 1.0 and diffTime <= 1.2:
            targets[angle].color = colors.red3L
        elif diffTime > 1.2 and diffTime <= 1.4:
            targets[angle].color = colors.red4L
        elif diffTime > 1.4 and diffTime <= 1.5:
            targets[angle].color = colors.red5L
        elif diffTime > 1.5 and diffTime <= 1.7:
            targets[angle].color = colors.red6L
        elif diffTime > 1.7:
            del targets[angle]
            

    # update the screen
    pygame.display.update()
    
