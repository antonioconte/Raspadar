import RPi.GPIO as GPIO
# from gpiozero import LED
from config import serverName, serverPort
import socket
import time
import numpy as np
import sys
import os

ITERATION = 10
MIN = ITERATION * 20 / 100
MAX = ITERATION - MIN
CYCLE = 181
TOLLERATION = 2.0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 19   # ARANCIO
ECHO = 26   # GIALLO
SERVO = 4
LASER = 17

#blue = LED(22)

# GPIO.setup(SERVO, GPIO.OUT)
# GPIO.setup(LASER, GPIO.OUT)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# p = GPIO.PWM(SERVO, 50)
# dc = 2.5
# p.start(dc)

staticElement = {}


def measure():
    GPIO.output(TRIG, False)
    GPIO.output(TRIG, True)  # Set TRIG as HIGH
    time.sleep(0.00001)
    GPIO.output(TRIG, False)  # Set TRIG as LOW

    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
        pulse_start = time.time()  # Saves the last known time of LOW pulse

    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
        pulse_end = time.time()  # Saves the last known time of HIGH pulse

    pulse_duration = pulse_end - pulse_start  # Get pulse duration to a variable

    distance = pulse_duration * 17150
    distance = round(distance, 2)  # Round to two decimal points
    if distance > 50:
        distance = 51
    return distance


def measure_average():
    stack = []
    for i in range(ITERATION):
        dist = measure()
        stack.append(float(dist))
    stack.sort()
    nuovo_stack = stack[int(MIN):int(MAX)]
    avg = float(np.mean(nuovo_stack))
    avg = round(avg, 2)
    return avg


def config_servo(angle):
    dc = angle * 2 / 45.0 + 2.5
    p.ChangeDutyCycle(dc)


def send_message(message, angle):
    message = str(message)+"@"+str(angle)
    message = message.encode('utf-8')
    clientSocket.sendto(message, (serverName, serverPort))


def find_element(array1, array2):
    for i in range(CYCLE):
        firstArrayElement = array1[i]
        secondArrayElement = array2[CYCLE-i-1]
        difference = abs(firstArrayElement-secondArrayElement)
        if(firstArrayElement != 51 and difference < TOLLERATION):
            msg = str("Same Value: " + str(firstArrayElement) +
                      " - " + str(secondArrayElement))
            # Add element
            staticElement[i] = firstArrayElement
            #send_message(msg, i)
    print(len(staticElement))


first_index = []
second_index = []


def sendAngleLaser(dict):
    if len(dict) == 0:
        print("Nessun Valore Minimo")
        return

    angleLaser, distance = min(dict.items(), key=lambda x: x[1])
    print("VALORE MINIMO ----> Angolo:", angleLaser, "Distanza: ", distance)

    # send_message(str(distance),str(angleLaser))
    # Move Servo
    # p.ChangeDutyCycle(angleLaser)


try:
    for angle in range(0, CYCLE):
        # LED ON
        # blue.on()
        # config_servo(angle)
        dist = measure_average()
        # dist = measure()
        first_index.append(dist)
        send_message(dist, angle)
        print(angle, " - ", dist)
        time.sleep(0.05)

    for angle in range(CYCLE-1, -1, -1):
        # config_servo(angle)
        dist = measure_average()
        # dist = measure()
        second_index.append(dist)
        send_message(dist, angle)
        print(angle, " - ", dist)
        time.sleep(0.05)

    # LED OFF
    # blue.off()
    find_element(first_index, second_index)
    sendAngleLaser(staticElement)


except KeyboardInterrupt:
    print("Stop")

finally:
    # GPIO.output(LASER, GPIO.LOW)
    # p.ChangeDutyCycle(2.5)
    time.sleep(1)
    # p.stop()
    clientSocket.close()
    GPIO.cleanup()

sys.exit()
