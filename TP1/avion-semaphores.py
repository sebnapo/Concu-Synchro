
#
#   Simulation d'une usine d'assemblage d'avions
#


#   L'usine est composée d'un ensemble de chaines séquentielles de montages
#   qui sont autonomes et fonctionnent en parallèle:
#   - 1 chaine de production de carlingues
#   - 1 chaine de production d'ailes
#   - 1 chaine de production de roues
#   - 1 chaine de production de moteurs
#   - 1 chaine d'assemblage 1 x carlingue + 2 x ailes
#   - 1 chaine d'assemblage 1 x 1xcarlingue+2xailes + 3 x roues
#   - 1 chaine d'assemblage de l'avion complet : 1xcarlingue+2xailes+3xroues+2xmoteurs
#


#   Proposez une synchronisation des chaines de montage à l'aide de sémaphores


import multiprocessing
import threading
import time
import random
tprint = print
from tprint import tprint

nbAvions=5

chaines = ["aile", "roue", "carlingue", "moteur", "carlingue1Ailes2", "carlingue1Ailes2Roues3", "avion"]
nbProduction=dict( {chaine:0 for chaine in chaines})


# Définition les sémaphores de synchronisation

SC = threading.Semaphore(0)
SA = threading.Semaphore(0)
SR = threading.Semaphore(0)
SM = threading.Semaphore(0)
SA1 = threading.Semaphore(0)
SA2 = threading.Semaphore(0)
SAv = threading.Semaphore(0)
# A Compléter...


def carlingue():
    for i in range(nbAvions):
        time.sleep(random.randint(0, 3))
        nbProduction["carlingue"] += 1
        tprint( 'Une carlingue est achevée ({})'.format(i+1))
        SC.release()

def aile() :
    for i in range(nbAvions*2):
        time.sleep(random.randint(0, 2))
        nbProduction["aile"] += 1
        tprint( 'Une Aile est achevée ({})'.format(i+1))
        SA.release()
        
def moteur():
    for i in range(nbAvions*2):
        time.sleep(random.randint(0, 1))
        nbProduction["moteur"] += 1
        tprint( 'Un moteur est achevé ({})'.format(i+1))
        SM.release()
        
def roue():
    for i in range(nbAvions*3):
        time.sleep(random.randint(0, 2))
        nbProduction["roue"] += 1
        tprint( 'Une roue est achevée ({})'.format(i+1))
        SR.release()

def carlingue1Ailes2():
    for i in range(nbAvions):
        SC.acquire()
        SA.acquire()
        SA.acquire()
        time.sleep(random.randint(0, 3))
        nbProduction["carlingue1Ailes2"] += 1
        tprint( 'Un assemblage 1 carlingue avec 2 ailes est achevé ({})'.format(i+1))
        SA1.release()

def carlingue1Ailes2Roues3():
    for i in range(nbAvions):
        SR.acquire()
        SR.acquire()
        SR.acquire()
        SA1.acquire()
        time.sleep(random.randint(0, 3))
        nbProduction["carlingue1Ailes2Roues3"] += 1
        tprint( 'Un assemblage 1 carlingue et 2 ailes avec 3 roue est achevé ({})'.format(i+1))
        SA2.release()


def avion():
    for i in range(nbAvions):
        SA2.acquire()
        time.sleep(random.randint(0, 3))
        nbProduction["avion"] += 1
        tprint( 'Un avion est achevé ({})'.format(i+1))
        SAv.release()

#
#  Test de l'usine d'assemblage d'avion
#

tprint('Demarrage de l\'usine')

# Création des Thread de chaine de production
threads=dict()
for chaine in [carlingue, aile, moteur, roue, carlingue1Ailes2, carlingue1Ailes2Roues3, avion ]:
    print(chaine.__name__)
    threads[chaine]=threading.Thread(target=chaine)

# Démarrage des threads
for t in threads.values() :
    t.start()

# Attente de terminaison des threads
for t in threads.values() :
    t.join()

tprint('Arret de l\'usine')

