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
#Creo funzione che apra un file
def file_to_DFG(file):
    file = open(file, "r+")
    DFG = pd.read_csv(file, names = ['Val', 'Oper', 'CLK'], engine = 'python', delimiter=";")
    return DFG

def dict_for_lyfe_cycle(dict):
    for i in range(len(DFG)):
        if DFG['Val'][i] not in dict:
            dict[DFG['Val'][i]] = DFG['CLK'][i]
        else:
            dict[DFG['Val'][i]] = DFG['CLK'][i] - dict[DFG['Val'][i]]
    return dict

def register(dict):
    #Determino il numero di registri che si utilizzano
    num_clock = max(list(dict.values()))
    life_cycle = []
    for i in range(int(num_clock)):
        life_cycle.append([])

    for node in range(0, len(dict.keys())):
        if len(list(dict.values())[node]) == 1:
            cycle = int(list(dict.values())[node])
            life_cycle[cycle - 1].append(list(dict.keys())[node])
        elif len(list(dict.values())[node]) > 1:
            for element in list(dict.values())[node]:
                if element != ',':
                    cycle = int(element)
                    life_cycle[cycle - 1].append(list(dict.keys())[node])
    return life_cycle

DFG = file_to_DFG("DFG1.txt") #Creo DFG dato un file di testo
dizionario = dict_for_lyfe_cycle(DFG) #Creo dizionario con le variabili e i rispettivi cicli di clock
life_cycle = register(dizionario) #Creo lista con i cicli di clock e le variabili attive in quel ciclo
for element in range(len(life_cycle)):
    print("Ciclo di clock: ", element + 1, "Variabili attive: ", life_cycle[element])
