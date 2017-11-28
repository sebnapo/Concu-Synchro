import multiprocessing
import threading
import time
import random
tprint = print
# A décommenter pour synchroniser l'affichage tprint()
from tprint import tprint

#
#   Probleme d'interblocage: l'étreinte fatale (Deadlock)
#

# Les semaphores
feuille = threading.Semaphore(1)
crayon = threading.Semaphore(1)
# A completer...




# Threads T1
def thread_T1() :

    tprint( 'Debut du thread T1')

    # A completer...

    # prise d'un jeton dans le semaphore feuille
    tprint( 'T1 : Demande P(feuille})')
    feuille.acquire()
    tprint( 'T1 : Obtient P(feuille})')

    time.sleep(random.randint(0, 3))
    
    # prise d'un jeton dans le semaphore crayon
    tprint( 'T1 : Demande P(crayon)' )
    crayon.acquire()
    tprint( 'T1 : Obtient P(crayon})')



    # Debut de section critique
    tprint( 'T1 : feuille et crayon obtenus')
    tprint( 'T1 : dessine...')

    # restitution d'un jeton dans le semaphore crayon
    tprint( 'T1 : V(crayon)' )
    crayon.release()

    # restitution d'un jeton dans le semaphore feuille
    tprint( 'T1 : V(feuille})')
    feuille.release()


# Threads T2
def thread_T2() :

    tprint( 'Debut du thread T2')

    time.sleep(random.randint(0, 3))
    
    # prise d'un jeton dans le semaphore crayon
    tprint( 'T2 : Demande P(feuille)' )
    feuille.acquire()
    tprint( 'T2 : Obtient P(feuille})')

    
    # prise d'un jeton dans le semaphore feuille
    tprint( 'T2 : Demande P(crayon})')
    crayon.acquire()
    tprint( 'T2 : Obtient P(crayon})')



    # Debut de section critique
    tprint( 'T2 : feuille et crayon obtenus')
    tprint( 'T2 : dessine...')

    # restitution d'un jeton dans le semaphore crayon
    tprint( 'T2 : v(feuille)' )
    feuille.release()

    # restitution d'un jeton dans le semaphore feuille
    tprint( 'T2 : V(crayon})')
    crayon.release()




  
# Création des Thread
t1=threading.Thread(target=thread_T1)
t2=threading.Thread(target=thread_T2)

tprint('Debut du test')

# Démarrage des threads
for t in [t1,t2]:
    t.start()

# Attente de terminaison des threads
for t in [t1,t2]:
    t.join()

tprint('Fin du test')

