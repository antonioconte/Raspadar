import time
import RPi.GPIO as GPIO
import numpy as np
from config import serverName, serverPort
import socket
import sys

ITERATION = 40
MIN = ITERATION * 20 / 100
MAX = ITERATION - MIN

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 19   # ARANCIO
ECHO = 26   # GIALLO
SERVO = 4
LASER = 17

GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(LASER, GPIO.OUT)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

p = GPIO.PWM(SERVO, 50)
# dc = Length / Period
dc = 7
p.start(dc)


def computation_distance(pulse_duration):
    # Multiply pulse duration by 17150 to get distance
    distance = pulse_duration * 17150
    distance = round(distance, 2)  # Round to two decimal points
    return distance


def measure():
    GPIO.output(TRIG, False)
    GPIO.output(TRIG, True)  # Set TRIG as HIGH
    time.sleep(0.0001)  # Delay of 0.0001 seconds
    GPIO.output(TRIG, False)  # Set TRIG as LOW

    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
        pulse_start = time.time()  # Saves the last known time of LOW pulse

    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
        pulse_end = time.time()  # Saves the last known time of HIGH pulse

    pulse_duration = pulse_end - pulse_start  # Get pulse duration to a variable
    return computation_distance(pulse_duration)


def measure_average():
    stack = []
    for i in range(ITERATION):
        dist = measure()
        stack.append(float(dist))

    stack.sort()
    nuovo_stack = stack[int(MIN):int(MAX)]
    avg = np.mean(nuovo_stack)
    avg = round(avg, 2)
    return avg


def config_servo(angle):
    angle = 180 - angle
    dc = 1.0 / 18.0 * angle + 2
    p.ChangeDutyCycle(dc)


def send_message(message, angle):
    message = str(message)+"@"+str(angle)
    message = message.encode('utf-8')
    clientSocket.sendto(message, (serverName, serverPort))


# first_dictionary_180 = {}
try:
    print("LED ON")
    GPIO.output(LASER, GPIO.HIGH)

    for angle in range(0, 180):
        config_servo(angle)
        dist = measure_average()
        # first_dictionary_180[angle] = dist
        send_message(dist, angle)
        print(angle)
        time.sleep(0.5)

    print("Finish")

except KeyboardInterrupt:
    print("Stop")

finally:
    GPIO.output(LASER, GPIO.LOW)
    clientSocket.close()
    GPIO.cleanup()

sys.exit()
