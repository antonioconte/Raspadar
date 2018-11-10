import numpy as np
import pandas as pd

def avgfun(l):
    l = l[20:80]
    avg =  np.mean(l)
    return round(avg,2)

directory = "Misure/"
materials = ["Legno","Vetro","Plastica","Ferro","Carta"]
distance = [str(i) for i in range(5,45,5)]
dict = {}
for m in materials:
    avg = []
    for d in distance:
        mList = []
        file = directory + m + "-" + d + ".csv"
        data = pd.read_csv(file) 
        mList = list(data['Misura'])
        avg.append(avgfun(mList))
    dict[m] = avg

df = pd.DataFrame(dict)

df.to_csv("Average.csv", encoding='utf-8', index=False)