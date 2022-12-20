# Ottimizzazione_Registri

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

Progetto sull'ottimizzazione dei registri utilizzando graph coloring sul grafo di incompatibilità.
Il programma riceve in ingresso un file .txt, contenente al suo interno: 
1) Variabile;
2) Operazione assegnata alla variabile;
3) Cicli di clock in cui rimane in vita.

![FILE TXT](https://user-images.githubusercontent.com/115625305/208668971-0a221c70-cdbb-46c1-8d5d-dc99049bbbb0.png)


Per disegnare il grafo di incompatibilità [Grafo che rappresenta un vertice per ogni variabile e un arco fra due variabili se queste sono attive nello stesso ciclo di clock], bisogna prima determinare per ogni ciclo di clock, quali variabili sono attive, e quali no.
Utilizzando la funzione Incompatibility_graph(life_cycle), a cui passiamo una lista di liste contenente le variabili attive per ogni ciclo di clock, riusciamo 
così a disegnare il grafo di incompatibilità.


![Grafo di incompatibilità](https://user-images.githubusercontent.com/115625305/208670448-ab4315d1-7f65-4175-a9cb-a6de3f689e6b.png)


Da qui riusciamo a determinare il numero massimo di registri che possiamo utilizzare, andando a calcolare, per ogni ciclo di clock, quale tra questi ha il numero
massimo di operazioni attive in quel momento.

ES: [['u0', 'u1', 'u2', 'u3'],['u4', 'u5'],['u5', 'u6'],['u5', 'u7'],['u5', 'u8'],['u9']] --> Nel primo ciclo di clock ci sono attive le operazioni u0,u1,u2,u3, nel secondo ciclo di clock ci sono attive u4,u5 e così via. Per cui il numero di registri da utilizzare è 4.
                                                 
Una volta determinato il numero massimo di registri che si devono utilizzare, andiamo ad assegnare ad ognuno di essi le variabili, questo processo viene chiamato **binding**. 

Per effettuare questo compito esistono degli algoritmi euristici di tipo greedy, ma questo codice permette di andare ad inserire l'operazione nel primo registro
libero, senza vincoli di spazio. 

Una volta assegnato un colore ad ogni nodo, dove ogni nodo comunicante nel grafo di incompatibilità ha un colore diverso, lo rappresento graficamente, determinando
così per ogni registro quale operazione e quale colore è assegnato.

![Graph Coloring](https://user-images.githubusercontent.com/115625305/208671827-39b835c1-5c7c-4dc9-ae62-c7d6da45f917.png)

Infine, dato il coloring graph, passiamo alla descrizione RTL dell'algoritmo, rappresentandolo così a terminale. 

![RTL Description](https://user-images.githubusercontent.com/115625305/208673885-3bd2a507-da79-4a37-af4d-59b9362dc1b0.png)

*FUNZIONAMENTO CODICE*

Al run dello script python, chiederà a terminale di scrivere il file che si vuole utilizzare tra quelli proposti (ES: DFG6.txt).

![START](https://user-images.githubusercontent.com/115625305/208674486-c507a0cd-f044-4ead-abfd-45738582842f.png)

Nel caso in cui si voglia aggiungere un file proprio, bisogna seguire lo schema "variabile; operazione;clock", come mostrato nella prima figura. 

Consecutivamente stamperà il grafo di incompatibilità, a cui segue il coloring graph, e la descrizione RTL. 
