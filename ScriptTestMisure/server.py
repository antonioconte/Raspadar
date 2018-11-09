import socket as s
from config import addr, port
import pandas as pd
import numpy as np
import sys

if len(sys.argv) < 2:
    print("Filename .csv Mancante")
    exit()


def error_rate(l):
    l = l[20:80]
    max_v = l[len(l)-1]
    min_v = l[0]
    diff = (max_v - min_v) / 2
    avg =  np.mean(l)
    error_v =   diff / avg
    return round(error_v*100,2)

filename = "Misure/" + sys.argv[1] + ".csv"

server =  s.socket(s.AF_INET, s.SOCK_DGRAM)
server.bind((addr, port))

mList = []
while True:
    data, a = server.recvfrom(1024)
    if float(data) < 0:
        print("Stop")
        break
    mList.append(round(float(data),2))

mList.sort()
df = pd.DataFrame({"Misura": mList})
df.to_csv(filename, encoding='utf-8', index=False, columns=["Misura"])
print("> {}, ErrorRate: {}".format(filename,error_rate(mList)))

 

