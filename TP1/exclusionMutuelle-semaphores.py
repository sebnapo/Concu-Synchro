import multiprocessing
import threading
import time
import random
tprint = print
# A décommenter pour synchroniser l'affichage tprint()
from tprint import tprint



# boucle de répétition de chaque thread
NbCoups = 10

# ressource critique:
RC = 0

# Les semaphores
S1 = threading.Semaphore(1)


# Threads P1
def thread_P1(nom) :
    global RC
    tprint( '{nom} : Debut du thread nom={nom}'.format(nom=nom, pid=multiprocessing.current_process().pid, tid=threading.get_ident()))

    for i in range(NbCoups):
        time.sleep(random.randint(0, 3))
        # P()
        S1.acquire()
        # Debut de section critique
        tprint( '{nom} : Debut de section critique'.format(nom=nom))

        a = RC
        time.sleep(random.randint(0, 3))
        RC = a + 1
        tprint( '{nom} : \t (i={i}) RC={RC}'.format(nom=nom, i=i, RC=RC) )

        tprint( '{nom} : Fin de section critique'.format(nom=nom))
	# fin de section critique
	# V()
        S1.release()


    tprint( '{nom} : Fin du thread'.format(nom=nom))



# Threads P2
def thread_P2(nom) :
    global RC
    tprint( '{nom} : Debut du thread nom={nom}'.format(nom=nom, pid=multiprocessing.current_process().pid, tid=threading.get_ident()))

    for i in range(NbCoups):
        time.sleep(random.randint(0, 3))
        #P()
        S1.acquire()

        # Debut de section critique
        tprint( '{nom} : Debut de section critique'.format(nom=nom))

        b = RC
        time.sleep(random.randint(0, 3))
        RC = b + 2
        tprint( '{nom} : \t (i={i}) RC={RC}'.format(nom=nom, i=i, RC=RC) )

        tprint( '{nom} : Fin de section critique'.format(nom=nom))
	# fin de section critique
        # V()
        S1.release()

    tprint( '{nom} : Fin du thread'.format(nom=nom))




# Création des Thread
P1 = threading.Thread(target=thread_P1, args=("P1",))
P2 = threading.Thread(target=thread_P2, args=("P2",))

tprint('Debut du test')

# Démarrage des threads
for t in [P1, P2]:
    t.start()

# Attente de terminaison des threads
for t in [P1,P2]:
    t.join()

tprint('Fin du test')

