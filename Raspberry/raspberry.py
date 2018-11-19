from gpiozero import LED, Buzzer
import RPi.GPIO as GPIO
import socket
import time
import signal
import sys
import numpy as np


# Socket setup
UDP_IP_ADDRESS = "192.168.1.102"
UDP_PORT_NO = 12000
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

timeSleep = 0.04
maxRange = 180
minRange = 0

angle = 0.0
status = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

trig = 19
echo = 26

green = LED(17)
yellow = LED(18)
red = LED(22)

buzzer = Buzzer(5)

# set GPIO input and output channels Distance Sensor
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)


relevations = []

def buzzSlow():
    buzzer.beep(0.2, 0.4)
    time.sleep(0.6)

def buzzFast():
    buzzer.beep(0.1, 0.1)
    time.sleep(0.6)

def green_light():
    green.on()
    yellow.off()
    red.off()
    buzzer.off()

def yellow_light():
    green.off()
    #yellow.blink(0.2, 0.4)
    yellow.on()
    red.off()
    #buzzSlow()

def red_light():
    green.off()
    yellow.off()
    #red.blink(0.1, 0.1)
    red.on()
    #buzzFast()

def led_allert(distance):
    if meanDistance >= 25:
        green_light()
    elif 10 < meanDistance < 25:
        yellow_light()
    elif meanDistance <= 10:
        red_light()


try:
    while True:

        # set Trigger to HIGH
        GPIO.output(trig, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(trig, False)

        startTime = time.time()
        stopTime = time.time()

        # save start time
        while 0 == GPIO.input(echo):
            startTime = time.time()

        # save time of arrival
        while 1 == GPIO.input(echo):
            stopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = stopTime - startTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        NowDistance = (TimeElapsed * 34300) / 2

        for n in range(100):
            relevations += [NowDistance]

        dataExtracted = np.array(relevations[20:80])
        meanDistance = sum(dataExtracted)/len(dataExtracted)

        relevations = []
        dataExtracted = []

        #print("Distance: %.1f cm -> %.6f" % (distance, TimeElapsed))
        led_allert(meanDistance)


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

        Message = str(round(meanDistance,2))+"@"+str(angle)
        
        clientSock.sendto(Message.encode("ascii"), (UDP_IP_ADDRESS, UDP_PORT_NO))
        time.sleep(timeSleep)
        

except KeyboardInterrupt:
    print("GoodBye")
    pass
