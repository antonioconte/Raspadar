import numpy as np
import pandas as pd

def error_rate(l):
    l = l[20:80]
    max_v = l[len(l)-1]
    min_v = l[0]
    diff = (max_v - min_v) / 2
    avg =  np.mean(l)
    error_v =   diff / avg
    return round(error_v*100,2)


directory = "Misure/"
materials = ["Legno","Vetro","Plastica","Ferro","Carta"]
distance = [str(i) for i in range(5,45,5)]
dict = {}
for m in materials:
    errorList = []
    for d in distance:
        mList = []
        file = directory + m + "-" + d + ".csv"
        data = pd.read_csv(file) 
        mList = list(data['Misura'])
        errorList.append(error_rate(mList))
    dict[m] = errorList

df = pd.DataFrame(dict)

df.to_csv("ErrorRate.csv", encoding='utf-8', index=False)