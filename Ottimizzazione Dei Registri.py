#PROGETTO LINGUAGGI DI DESCRIZIONE DELL'HARDWARE SULL'OTTIMIZZAZIONE DEI REGISTRI

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
Dato un data-flow graph con scheduling, si chiede di implementare l’ottimizzazione
dei registri tramite graph-coloring. In particolare, il programma riceve in ingresso 
un file di testo con la descrizione dell’algoritmo in cui ciascuna operazione e annotata 
con il ciclo di clock in cui viene eseguita e la risorsa funzionale che la esegue (binding).
A questo punto per ogni variabile utilizzata (a sinistra degli assegnamenti), si calcola il tempo
di vita e da questo grafo si ottiene il numero di colori (registri) da utilizzare per il graph coloring
e il grafo di incompatibilita delle variabili. Per colorare quest’ultimo esistono delle tecniche esatte, ma qui si suggerisce
di utilizzare un euristico di tipo greedy. Si tratta semplicemente di definire un ordinamento per i vertici e uno per i colori.
Si parte dal primo vertice e si procede assegnando a ciascun vertice un colore fra quelli diversi da quelli dei vertici adiacenti
a quello considerato. Dopo aver fatto questa operazione, si chiede di scrivere la tabella con la descrizione RTL delle operazioni.
'''

file = open("DFG1.txt", "r+")

DFG = pd.read_csv(file, names = ['Val', 'Oper', 'CLK'], engine = 'python', delimiter=";")

#Definisco quanti cicli di clk ci sono nel DFG
CLK = DFG['CLK'].values
CLK_number = []
for element in CLK:
    if element not in CLK_number:
        CLK_number.append(element)
print("Nel DFG ci sono", CLK_number[-1], "cicli di clock")
number_CLK = []
for i in range(1, int(CLK_number[-1]) + 1):
    number_CLK.append(i)
    
CLK_plot = np.array(number_CLK)
x = np.arange(0,20) 
y = []
for element in CLK_plot:
    for v in range (0, 20):
        y.append(element)

#Definisco quante operazioni ci sono nel DFG
VAL = DFG['Val'].values


print(DFG['CLK'].values)
for i in range(0, int(len(VAL))):
    print("Loperazione", DFG['Val'].iloc[i],":", DFG['Oper'].iloc[i], "si mantiene nel/i ciclo/i", DFG['CLK'].iloc[i])

c = 0
for i in range(0, int(len(VAL))):
    plt.plot(c, DFG['CLK'].iloc[i], "bo")
    c += 1

print("CIAO")
    

plt.plot(x, y[:20])
plt.plot(x, y[20:40])
plt.plot(x, y[40:60])
plt.plot(x, y[60:80])
plt.plot(x, y[80:100])
plt.ylabel("CLOCK")
plt.show()








