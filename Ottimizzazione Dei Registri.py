#PROGETTO LINGUAGGI DI DESCRIZIONE DELL'HARDWARE SULL'OTTIMIZZAZIONE DEI REGISTRI

import numpy as np
import pandas as pd
import networkx as nx
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

def decision_file():
    y_n = "n"
    
    while y_n != "y":
        print("HAI A DISPOSIZIONE DIVERSI FILE DA CUI SCEGLIER, CHE VANNO DA DFG1.txt a DFG9.txt, DIGITA QUELLO CHE VORRESTI UTILIZZARE \nAd esempio DFG5.txt...")
        DFG_chosen = input()
        print("SEI SICURO DELLA TUA SCELTA? \nDigita y/n...")
        y_n = input()
    
    return DFG_chosen

#Creo funzione che apra un file
def file_to_DFG(file):
    file = open(file, "r+")
    DFG = pd.read_csv(file, names = ['Val', 'Oper', 'CLK'], engine = 'python', delimiter=";")
    print("------------------------------------------------")
    print("         IL FILE SCELTO E' IL SEGUENTE          ")
    print(DFG)
    print("------------------------------------------------")
    return DFG

def dict_for_lyfe_cycle(DFG):
    dict = {}
    for i in range(len(DFG)):
        if DFG['Val'][i] not in dict:
            dict[DFG['Val'][i]] = str(DFG['CLK'][i])
        else:
            dict[DFG['Val'][i]] = DFG['CLK'][i] - dict[DFG['Val'][i]]
    return dict

#CORREGGERE ERRORE IN CREAZIONE LISTA QUANDO HO UN CICLO DI CLOCK PER OGNI OPERAZIONE
def register(dict):
    #Determino il numero di registri che si utilizzano
    num_clock = max(list(dict.values()))
    life_cycle = []
    for i in range(int(num_clock)):
        life_cycle.append([])
    
    for node in range(0, len(dict.keys())):
        lista = list(dict.values())
        if len(lista[node]) < 2:
            cycle = int(list(dict.values())[node])
            life_cycle[cycle - 1].append(list(dict.keys())[node])
        elif len(list(dict.values())[node]) > 1:
            for element in list(dict.values())[node]:
                if element != ',':
                    cycle = int(element)
                    life_cycle[cycle - 1].append(list(dict.keys())[node])
        
    return life_cycle

def Number_of_register(life_cycle):
    #Determino il numero di registri che si utilizzano 
    num_register = 0
    comparison = 0
    for clock in life_cycle:
        for operation in clock:
            if operation != ',':
                comparison += 1
        if num_register <= comparison:
            num_register = comparison
            comparison = 0
        else:
            comparison = 0    
    return num_register     
                

def Incompatibility_Graph(life_cycle):
    fig, axs = plt.subplots(1, len(life_cycle))
    fig.suptitle('Grafo di incompatibilità')
    for i, clock in enumerate(life_cycle):
        G = nx.Graph()
        for operation in clock:
            if operation != ',':
                G.add_node(operation, size = 2)
        for operation in clock:
            if operation != ',':
                for operation2 in clock:
                    if operation2 != ',':
                        if operation != operation2:
                            G.add_edge(operation, operation2)
        nx.draw(G, with_labels = True, ax = axs[i])    
    
    return G, plt

#Crea la directori a cui associa ad ogni operazione (chiave) le operazioni incompatibili (valore)
def dict_incompatibility(life_cycle):
    dict = {}
    for i, clock in enumerate(life_cycle):
        for operation in clock:
            if operation != ',':
                if operation not in dict:
                    dict[operation] = []
                for operation2 in clock:
                    if operation2 != ',':
                        if operation2 not in dict[operation]:
                            if operation != operation2:
                                dict[operation].append(operation2)
    return dict

#Determina se un'operazione è compatibile con un registro (quali nodi vanno dello stesso colore)
def compatible(register, dict, operation):
    x = 0
    for element in register:
        if element == operation:
            continue
        elif operation in list(dict[element]):
            x = 0
            break
        else:
            x = 1
    if x == 1:
        return True
    else:  
        return False

#Creazione dei registri
def register_optimization(life_cycle, dict, num_register):
    register_optimized = []
    operation_used = []
    for i in range(0, num_register):
        register_optimized.append([])   
    for clock in life_cycle:
        for operation in clock:
            for register in register_optimized:
                if operation not in operation_used:
                    if register == []:
                        register.append(operation)
                        operation_used.append(operation)
                        break
                    elif operation in register:
                        break
                    else:
                        add = compatible(register, dict, operation)
                        if add == True:
                            register.append(operation)
                            operation_used.append(operation)
                        else: 
                            continue    
                else: 
                    continue                    
    return register_optimized

def register_optimization_2(life_cycle, dict, num_register, max_operation):
    register_optimized = []
    operation_used = []
    for i in range(0, num_register):
        register_optimized.append([])   
    for clock in life_cycle:
        for operation in clock:
            for register in register_optimized:
                if len(register) < int(max_operation):
                    if operation not in operation_used:
                        if register == []:
                            register.append(operation)
                            operation_used.append(operation)
                            break
                        elif operation in register:
                            break
                        else:
                            add = compatible(register, dict, operation)
                            if add == True:
                                register.append(operation)
                                operation_used.append(operation)
                            else: 
                                continue    
                    else: 
                        continue                 
    return register_optimized

def coloring_graph(graph, registri, life_cycle):
    color = list(np.random.choice(range(256), size = len(registri)))
    dict_color = {}

    #Assegno ad ogni nodo il proprio colore 
    for clock in life_cycle:
        for element in clock:
            j=0
            for registro in registri:
                if element in registro:
                    dict_color[element] = color[j]
                else: 
                    j+=1
    fig, axs = plt.subplots(1, len(life_cycle))
    fig.suptitle('COLORING GRAPH')
    for i, clock in enumerate(life_cycle):
        G = nx.Graph()
        for operation in clock:
            if operation != ',':
                G.add_node(operation, size = 2)
        for operation in clock:
            if operation != ',':
                for operation2 in clock:
                    if operation2 != ',':
                        if operation != operation2:
                            G.add_edge(operation, operation2)
        nx.set_node_attributes(G, dict_color, 'color')
        nx.draw(G, with_labels = True, ax = axs[i], node_color = [color for _, color in nx.get_node_attributes(G, 'color').items()])
    print("La corrispondenza nodi-colore è: ", dict_color)
    return plt.show(), color

def RTL_Description(registri, color, life_cycle, DFG):
    dict = {}
    dict2 = {}
    dict_operation = {}

    nome_registro = []


    for i in range(len(DFG)):
        if DFG['Val'][i] not in dict_operation:
            dict_operation[DFG['Val'][i]] = DFG['Oper'][i]
        else:
            dict_operation[DFG['Val'][i]] = DFG['Oper'][i] - dict_operation[DFG['Oper'][i]]

    for i in range(0,len(registri)):
        nome_registro.append("R" + str(i))

    dict["Colore"] = list(color)
    dict["Registro"] = nome_registro
    dict["Variabili attive"] = registri


    operazioni = []
    for i in range(0,len(life_cycle)):
        operazioni.append([])

    #print(dict_operation)
    i = 0
    for clock in life_cycle:
        j = 0
        for element in clock:
            operazioni[i].append(dict_operation[element])
            j+=1
        i+=1
    
    

    dict2["Clock"] = list(range(1,int(max(DFG["CLK"]))+1))
    dict2["Operazioni"] = operazioni 

    #print(dict2)

    rtl_1 = pd.DataFrame(dict)
    rtl_2 = pd.DataFrame(dict2)
    print("-------------------------------------")
    print("           RTL DESCRIPTION           ")
    print("-------------------------------------")
    print(rtl_2, "\n", rtl_1)


file = decision_file()
DFG = file_to_DFG(file) #Creo DFG dato un file di testo
dizionario = dict_for_lyfe_cycle(DFG) #Creo dizionario con le variabili e i rispettivi cicli di clock
life_cycle = register(dizionario) #Creo lista con i cicli di clock e le variabili attive in quel ciclo
register = Number_of_register(life_cycle) #Determino il numero di registri che si utilizzano
for element in range(len(life_cycle)):
    print("Nel ciclo di clock: ", element + 1, "le variabili attive sono: ", life_cycle[element])

print("IL NUMERO DI REGISTRI NECESSARIO PER IL COLORING GRAPH E': ", register)

graph, figure = Incompatibility_Graph(life_cycle) #Creo il grafo di incompatibilità
figure.show()

incomp_dict = dict_incompatibility(life_cycle) #Creo dizionario con le variabili e le rispettive incompatibilità
#print("Quante operazioni vuoi al massimo per ogni registro sapendo che all'interno ci sono ", register, "registri")
#max_operation = input(" ")
registri = register_optimization(life_cycle, incomp_dict, register) #Ottimizzo il numero di registri, se voglio decidere quante operazioni mettere nel registro, inserire la variabile di input

print("------------------------------------------------")
for i in range(0,len(registri)):
    print("Il registro ",i,"contiene le seguenti operazioni --> ", registri[i])


final_graph, color = coloring_graph(figure, registri, life_cycle)
rtl = RTL_Description(registri, color,life_cycle, DFG)
#optimezed_register = coloring_graph(graph, register) #Coloro il grafo di incompatibilità
