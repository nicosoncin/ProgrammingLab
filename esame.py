#ESAME LABORATORIO DI PROGRAMMAZIONE

#AUTORE: Nicolò Soncin
#CORSO: INTELLIGENZA ARTIFICIALE

#creo la classe per le eccezioni
class ExamException(Exception):

    pass


class CSVTimeSeriesFile:


    def __init__(self, name):
        
        # Instanzio la classe sul nome del file tramite la variabile "name"
        self.name = name


    def get_data(self):

        #creo una lista che mi servirà per il controllo delle ececzioni
        controllo_orari=[]
        # Inizializzo una lista vuota per salvare poi tutte le liste con i valori
        lista= []
        # Tento di aprire il file, se il file non esiste o non è leggibile alzo un'eccezione
        try:
            my_file = open(self.name, 'r')
        except ExamException as e:
            # Stampa in caso di errore:
            print('Errore nella lettura del file: "{}"'.format(e))
            #In caso di errore nell'apertura del file ritorno "niente"
            return None
        # Se il file è leggibile lo leggo linea per linea
        for line in my_file:

            #creo una lista temporanea nella quale aggiungerò poi i valori di orario e temperatura
            temp = []
            
            # Faccio lo split di ogni linea sulla virgola
            elements = line.split(',')

            if elements[0] != 'epoch':
                #metto try così se c'è una riga incompleta o nulla la salto e leggo quella successiva
                try:
                    # Setto la data ed il valore
                    orario  = elements[0]
                    valore = elements[1]
                except:
                    continue

                #provo a trasformare il valore dell'orario in intero, se non si può ccontinuo e salto la riga 
                try:
                    orario = float(orario)
                    orario = int (orario)
                except:
                    continue
                # Se la variabile "valore" non è convertibile in un valore numerico, passo alla linea successiva senza alzare un'eccezione
                try:
                    valore = (float(valore) or int(valore))
                except:
                    continue

                controllo_orari.append(orario)
                # Aggiungo alla lista temporanea i valori dell'orario e temperatura
                temp.append(orario)
                temp.append(valore)
                #Aggiungo alla lista finale la lista temporanea
                lista.append(temp)
                #Setto la lista temporanea vuota così al prossimo ciclo cambia e aggiungerò una lista diversa alla lista finale
                temp = []
        #se il file è vuoto non posso eseguire alcun calcolo, quindi alzo un'eccezione
        if len(lista) == 0:
            raise ExamException('il file è vuoto')
            return None
        #effettuo un controllo sui valori degli orari, se non sono in ordine o è presente un duplicato alzo un'eccezione
        #controllo un elemento della lista con gli orari con il valore successivo
        for x in range (0, len(controllo_orari)-1):
            for y in range (x + 1, len(controllo_orari)):
                if (controllo_orari[x] > controllo_orari [y]):
                    raise ExamException ('errore: i valori non sono in ordine') 
                    
                if (controllo_orari [x] == controllo_orari [y]):
                    raise ExamException ('errore: è presente un valore duplicato')
                     
        #PER STAMPARE LA LISTA DI LISTE:
        #print('[')        
        #for i in range (0, len(lista)):
        #    print(lista[i],",")
        #print(']')

        # Chiudo il file
        my_file.close()
        return lista
        
    

#time_series_file = CSVTimeSeriesFile(name = 'data.csv')
#time_series = time_series_file.get_data()




#creo una funzione per calcolare minimo, massimo, e valore medio
def calcoli(lista):
    #creo la lista nella quale inserirò i tre valori
    valori = []
    #inizializzo la variabile somma a 0 per il calcolo della media
    somma = 0

    if len(lista) == 0:
        raise ExamException('non ci sono abbastanza elementi da calcolare')
    #calcolo il minimo che all'inizio metto che sia uguale al primo valore della lista, così se trovo un valore più piccolo ciclando la lista, lo considero il nuovo minimo
    minimo = lista[0]
    for i in range(len(lista)):
        if lista[i] < minimo:
            minimo = lista[i]
    #calcolo il massimo che all'inizio metto che sia uguale al primo valore della lista, così se trovo un valore più grande ciclando la lista, lo considero il nuovo massimo
    massimo = lista[0]
    for i in range(len(lista)):
        if lista[i] > massimo:
            massimo=lista[i]

    #calcolo della media
    for i in range(0, len(lista)):
        somma += lista[i] 
        media = somma/(len(lista))

    valori.append(minimo)
    valori.append(massimo)
    valori.append(media)
    return valori
    


#creo la funzione che per ogni giorno mi salva i valori in una lista che viene poi aggiunta alla lista finale
def daily_stats(time_series):
    #la lista da considerare è come quella che mi arriva dalla classe
    lista = time_series
    #creo una lista temporanea
    temp = [] 
    #creo una lista vuota nella quale salvare il valore degli inizi di un nuovo giorno
    inizio_giorno = []
    #lista in cui salverò le liste con i dati di minimo, massimo e valor medio di tuuti i giorni
    valori_giornate = []
    #'aaa' è la prima lista della lista 'lista'
    aaa = lista[0]
    #tempo si trova alla prima posizione della lista 'aaa'
    tempo = aaa[0]
    #la temperatura si trova alla seconda posizione nella lista 'aaa'
    valori = aaa[1]
    #formula per calcolare se un orario è l'inizio di un giorno
    z = tempo - (tempo % 86400)
    #aggiungo l'inizio del primo giorno della lista 'lista' alla lista 'inizio_giorno' nella prima posizione 
    inizio_giorno.append(z)

    #ciclo per calcolare l'inizio di tutti i giorni della 'lista', di lunghezza massima 31 (giorni massimi in un mese)
    for i in range (0, 31):
        #aggiungo 86400, che è la durata in secondi di un giorno, al primo inizio di giorno che ho trovato, che è già nella prima posizione, avendolo aggiunto prima alla lista 'inizio_giorno'
        #poi aggiungo i valori a questa lista
        inizio_giorno.append(inizio_giorno[i]+86400)

    
    #aggiungo alla lista temporanea 'temp' i valori minimo, massimo e valor medio per ogni giorno 
    for x in range(0, len(inizio_giorno)-1):  
        #guardo tutte le liste 'aaa' all'interno della lista 'lista' 
        for y in range(0, len(lista)):
            aaa = lista[y]
            tempo = aaa[0]
            valori = aaa[1]
            #aggiungo tutti valori delle temperature degli orari della liste 'aaa', compresi tra l'inizio di un giorno e l'altro, alla lista temporanea
            if (tempo >= inizio_giorno[x]) and (tempo < inizio_giorno[x+1]):
                #aggiungo alla lista temporanea i valori della temperatura per ogni giorno
                temp.append(valori)
        #aggiungo alla lista 'valori_giornate' la lista temporanea con il calcolo di minimo, massimo e valore medio per ogni giornata
        valori_giornate.append(calcoli(temp))
        #'svuoto' la lista temporanea così al prossimo ciclo inserisco nuovi valori 
        temp = []
    

    ##PER STAMPARE A SCHERMO LA LISTA CON LE LISTE DI MINIMO, MASSIMO E VALORE MEDIO PER OGNI GIORNO:
    #print('[')        
    #for i in range (0, len(valori_giornate)):
    #    print(valori_giornate[i],",")
    #print(']')

    return valori_giornate



#y = daily_stats(time_series)