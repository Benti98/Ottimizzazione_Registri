# Ottimizzazione_Registri
Utilizziamo algoritmi greedy per l'ottimizzazione dei registri di un DFG.

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
Il programma riceve in ingresso un file .txt contenente al suo interno: 
1) Variabile;
2) Operazione assegnata alla variabile;
3) Cicli di clock in cui rimane in vita.
{FOTO}

Per disegnare il grafo di incompatibilità {SPIEGAZIONE DI COSA E'} bisogna prima determinare per ogni ciclo di clock, quali variabili sono attive, e quali no.
Utilizzando la funzione Incompatibility_graph(life_cycle), a cui passiamo una lista di liste contenente le variabili attive per ogni ciclo di clock, riusciamo 
così a disegnare il grafo di incompatibilità.

Da qui riusciamo a determinare il numero massimo di registri che possiamo utilizzare, andando a calcolare, per ogni ciclo di clock, quale tra questi ha il numero
massimo di operazioni attive in quel momento.

ES: [[u0,u5,u10],[u7,u1],[u3,u4,u8,u9],[u2]] --> Nel primo ciclo di clock ci sono attive le operazioni u0,u5,u10, nel secondo ciclo di clock ci sono attive
                                                 u7,u1 e così via. Per cui il numero di registri da utilizzare è 4.
                                                 
Una volta determinato il numero massimo di registri che si devono utilizzare, andiamo ad assegnare ad ognuno di essi le variabili. 

Per effettuare questo compito esistono degli algoritmi euristici di tipo greedy, ma questo codice permette di andare ad inserire l'operazione nel primo registro
libero, senza vincoli di spazio. 

Una volta assegnato un colore ad ogni nodo, dove ogni nodo comunicante nel grafo di incompatibilità ha un colore diverso, lo rappresento graficamente, determinando
così per ogni registro quale operazione e quale colore è assegnato.
{FOTO}

Infine, dato il coloring graph, passiamo alla descrizione RTL {SPIEGAZIONE DI COSA E'} dell'algoritmo, rappresentandolo così a terminale. 

*FUNZIONAMENTO CODICE*

Al run dello script python, chiederà a terminale di scrivere il file che si vuole utilizzare tra quelli proposti (ES: DFG6.txt).

Nel caso in cui si voglia aggiungere un file proprio, bisogna seguire lo schema "variabile; operazione;clock", come mostrato in figura prima. 

Consecutivamente stamperà il grafo di incompatibilità, a cui segue il coloring graph, e la descrizione RTL. 
