import RPi.GPIO as GPIO
from gpiozero import LED
from config import serverName, serverPort
import socket
import time
import numpy as np
import sys
import os

ITERATION = 20
MIN = ITERATION * 20 / 100
MAX = ITERATION - MIN
CYCLE = 181
TOLLERATION = 2.0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# PIN
TRIG = 19
ECHO = 26
SERVO = 4
LASER = 13
blue = LED(22)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(LASER, GPIO.OUT)

p = GPIO.PWM(SERVO, 50)
# Move servo to initial position
dc = 10.5 
p.start(dc)

angleSleep = 0.05

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
time.sleep(3)

# StaticElement dictionar between first and second relevations 
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
    if distance > 50: #Out of Range
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

# Convert angle into DutyCycle and move servo
def config_servo(angle):
    dc = angle * 2 / 45.0 + 2.5
    p.ChangeDutyCycle(dc)

# Send distance, angle to radar
def send_message(distance, angle):
    message = str(distance)+"@"+str(angle)
    message = message.encode('utf-8')
    clientSocket.sendto(message, (serverName, serverPort))

# Find similar value between first and second relevation
def find_element(array1, array2):
    for i in range(CYCLE):
        firstArrayElement = array1[i]
        secondArrayElement = array2[CYCLE-i-1]
        difference = abs(firstArrayElement-secondArrayElement)
        if(firstArrayElement != 51 and difference < TOLLERATION):

            # Add element
            staticElement[i] = firstArrayElement

# First and Second revelations array
first_index = []
second_index = []

# Take angle and distance of min value of dictionar
# Send values to radar
# Move servo and Start Laser  
def sendAngleLaser(dict):
    if len(dict) == 0:
        print("Nessun Valore Minimo")
        return

    angleLaser, distance = min(dict.items(), key=lambda x: x[1])

    send_message(str(distance),str(CYCLE-angleLaser))
    # Move Servo
    config_servo(CYCLE-angleLaser)
    time.sleep(1)
    # Laser ON
    GPIO.output(LASER, GPIO.HIGH) 
    time.sleep(4)
    # Laser OFF
    GPIO.output(LASER, GPIO.LOW)


try:
    # Sx to Dx
    for angle in range(CYCLE-1, -1, -1):
        # LED ON
        blue.on()
        config_servo(angle)
        dist = measure()
        first_index.append(dist)
        send_message(dist, angle)
        time.sleep(angleSleep)

    time.sleep(1)
    
    # Dx to Sx
    for angle in range (0, CYCLE):
        config_servo(angle)
        dist = measure()
        second_index.append(dist)
        send_message(dist, angle)
        time.sleep(angleSleep)

    # Reset radar targets
    send_message(-1, -1)
    # LED OFF
    blue.off()
    find_element(first_index, second_index)
    sendAngleLaser(staticElement)

except KeyboardInterrupt:
    print("Stop")

finally:
    p.ChangeDutyCycle(10.5)
    time.sleep(1)
    p.stop()
    clientSocket.close()
    GPIO.cleanup()

