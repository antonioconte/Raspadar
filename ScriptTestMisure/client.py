import socket
from config import addr, port
import time  
import random
import RPi.GPIO as GPIO  # Import GPIO library

GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering
TRIG = 19  # GIALLO
ECHO = 26  # ARANCIONE

GPIO.setup(TRIG, GPIO.OUT)  # Set pin as GPIO out
GPIO.setup(ECHO, GPIO.IN)  # Set pin as GPIO in


def computation_distance(pulse_duration):
    # Multiply pulse duration by 17150 to get distance
    distance = pulse_duration * 17150
    distance = round(distance, 2)  # Round to two decimal points
    return distance


def measure():
    GPIO.output(TRIG, False) 
    GPIO.output(TRIG, True)  # Set TRIG as HIGH
    time.sleep(0.00001)  # Delay of 0.00001 seconds
    GPIO.output(TRIG, False)  # Set TRIG as LOW
    pulse_start = time.time()

    while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
        pulse_start = time.time()  # Saves the last known time of LOW pulse

    while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
        pulse_end = time.time()  # Saves the last known time of HIGH pulse

    pulse_duration = pulse_end - pulse_start  # Get pulse duration to a variable
    return computation_distance(pulse_duration)


def measure_average():
    # This function takes 3 measurements and
    # returns the average.
    distance1 = measure()
    # time.sleep(0.1)
    # distance2 = measure()
    # time.sleep(0.1)
    # distance3 = measure()
    # distance = distance1 + distance2 + distance3
    # distance = distance / 3
    return float(distance1)



client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for i in range(100):
    # dist = measure_average()
    dist = measure()
    client.sendto(str(dist),(addr,port))
    time.sleep(0.01)

client.sendto("-1",(addr,port))
GPIO.cleanup()