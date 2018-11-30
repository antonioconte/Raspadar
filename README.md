# Raspadar
Progetto di Fisica dei Sistemi Complessi AA 2017-18

### Raspberry

Gestisce il servomotore, calcola la distanza attraverso il sensore ad ultrasuoni HC-SR04, invia i dati al radar e punta l'oggetto più vicino rimasto invariato dalle due iterate
```console
foo@bar: ~ $ python client.py
```

### Radar

Visualizzazione grafica su radar del funzionamento del sistema

Risoluzioni:
  - 1600x820
  - 1000x600

```console
foo@bar: ~ $ python radar_[resolution].py
```
### Schema

<img src="https://github.com/antonioconte/Raspadar/blob/master/Schema/schema.png?raw=true" width="350">

### ScriptTestMisure

Utilizzato per fare test sull'accuratezza del sensore HC-SR04
#### client.py (Raspberry)
```console
foo@bar: ~ $ python client.py
```
#### server.py MATERIALE-CM (PC-LOCALE)
```console
foo@bar: ~ $ python3 server.py Legno-5
```
Crea un file "Legno-5.csv" nella cartella "Misure"

#### config.py
utilizzato sia dal client che dal server e contiene la porta e l'indizzo ip del server
```python
addr = "0.0.0.0"
port = 1234
```

