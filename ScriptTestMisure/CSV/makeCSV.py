import numpy as np
import pandas as pd

materials = ["Legno","Vetro","Plastica","Ferro","Carta"]
distance = [str(i) for i in range(5,45,5)]
for m in materials:
    dict = {"min": [],"max":[],"avg":[],"err":[]}
    for d in distance:
        data = pd.read_csv("../Misure/"+m+"-"+d+".csv") 
        data = data["Misura"][20:80]
        min_v = round(min(data),2)
        max_v = round(max(data),2)
        avg = round(np.mean(data),2)
        error_v = round((((max_v - min_v)/2)/avg)*100,2)
        dict["min"].append(min_v)
        dict["max"].append(max_v)
        dict["avg"].append(avg)
        dict["err"].append(error_v)

    df = pd.DataFrame(dict,columns=["min","max","avg","err"])
    df.to_csv(m+".csv", encoding='utf-8',index=False)


    
        
        