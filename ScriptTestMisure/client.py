import socket
import RPi.GPIO as GPIO  # Import GPIO library
import time  # Import time library

GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering

TRIG = 19  # GIALLO
ECHO = 26  # ARANCIONE

# print("Distance measurement in progress")

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
    time.sleep(0.1)
    distance2 = measure()
    time.sleep(0.1)
    distance3 = measure()
    distance = distance1 + distance2 + distance3
    distance = distance / 3
    return float(distance)

addr = "192.168.43.117"
port = 12000
msg = 124

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
l = []
for i in range(10):
    dist = measure_average()
    l.append(dist)
    # msg = "Distance: %.2f cm" % dist
    # msg = "Distance: %.2f cm"
    # client.sendto(str(msg),(addr,port))
    msg = "> " + str(i+1) + " iterazione!"
    client.sendto(str(msg),(addr,port))
    time.sleep(1)

res = "Min: [" + str(round(min(l),2)) +"] - Avg: [" + str(round(sum(l)/10.0,2)) + "] - Max: [" + str(round(max(l),2)) + "]"
client.sendto(str(res),(addr,port))
GPIO.cleanup()