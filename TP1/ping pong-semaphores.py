import multiprocessing
import threading
import time
import random
tprint = print
# A décommenter pour synchroniser l'affichage tprint()
from tprint import tprint



# liste des noms de threads à créer
# NomsThreads = ["PONG","PING"]
NomsThreads = ["PONG","PING","PING","PONG","PING","PONG","PONG","PING"]
# puis essayez avec:
# NomsThreads = ["PONG","PING","PING","PONG","PING","PONG","PONG","PING"]
threads = []

# boucle de répétition de chaque thread
NbCoups = 10

# ressource critique: 
chaine_ping_pong = ''

# Les semaphores
SPI = threading.Semaphore(1)
SPO = threading.Semaphore(0)



# Threads de type Ping (resp. Pong)
def thread_ping_pong(nom) :
    global chaine_ping_pong
    tprint( '{nom} : Debut du thread nom={nom}, pid={pid}, tid={tid}'.format(nom=nom, pid=multiprocessing.current_process().pid, tid=threading.get_ident()))

    for i in range(NbCoups):
        time.sleep(random.randint(0, 3))

	# A completer ...
        if nom is "PING" :
            SPI.acquire()
        else :
            SPO.acquire()
            

        # Debut de section critique
        tprint( '{nom} : Debut de section critique'.format(nom=nom))

        time.sleep(random.randint(0, 3))
        chaine_ping_pong = chaine_ping_pong + nom + ' '
        tprint( '{nom} : \t (i={i}) chaine_ping_pong={chaine_ping_pong}'.format(nom=nom, i=i, chaine_ping_pong=chaine_ping_pong) )

        tprint( '{nom} : Fin de section critique'.format(nom=nom))
	# fin de section critique

	# A completer ...
        if nom is "PING" :
            SPO.release()
        else :
            SPI.release()
            
    tprint( '{nom} : Fin du thread'.format(nom=nom))



  
# Création des Thread
for nom in NomsThreads:
    threads.append(threading.Thread(target=thread_ping_pong, args=(nom,)))
# ou
# threads = [threading.Thread(target=thread_ping_pong, args=(nom,)) for nom in NomsThreads]

tprint('Debut du test avec {nom}'.format(nom=NomsThreads))

# Démarrage des threads
for t in threads:
    t.start()

# Attente de terminaison des threads
for t in threads:
    t.join()

tprint('Fin du test')

