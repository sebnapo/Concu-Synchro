
#
#   Simulation d'une usine d'assemblage d'aeroplanes
#


#   L'usine est composée d'un ensemble de chaines séquentielles de montages
#   qui sont autonomes et fonctionnent en parallèle:
#   - 1 chaine de production de carlingues
#   - 1 chaine de production d'ailes
#   - 1 chaine de production de roues
#   - 1 chaine de production de moteurs
#   - 1 chaine d'assemblage 1 x carlingue + 2 x ailes
#   - 1 chaine d'assemblage 1 x 1xcarlingue+2xailes + 3 x roues
#   - 1 chaine d'assemblage de l'aeroplane complet : 1xcarlingue+2xailes+3xroues+2xmoteurs
#

#
#   Proposez une synchronisation des chaines de montage à l'aide de tampons producteurs consommateurs
#

import multiprocessing
import threading
import time
import random
from tampon_fifo import Tampon_fifo, tampon_est_plein, tampon_est_vide, tampon_nbElements
# A décommenter pour importer le tampon producteur consommateur protégé par moniteur
from producteur_consommateur_moniteur import MoniteurProdCons, moniteur_deposer, moniteur_retirer
tprint = print
# A décommenter pour synchroniser l'affichage tprint()
from tprint import tprint



class UsineAeroplane :
    def __init__(self, tailleMaxTamponsChaines=2):
        tailleMax = 10
        # Les chaines d'assemblage
        self.chaines = ["aile", "roue", "carlingue", "moteur", "carlingue1Ailes2", "carlingue1Ailes2Roues3", "aeroplane"]
        self.tailleMaxTamponsChaines = tailleMaxTamponsChaines
        # A completer: definir les tampons PC (bornés à tailleMax) entre les chaines servant à stocker les productions de chaque chaine
        self.tCarlingue = MoniteurProdCons(Tampon_fifo(tailleMax))
        self.tAile = MoniteurProdCons(Tampon_fifo(tailleMax))
        self.tRoue = MoniteurProdCons(Tampon_fifo(tailleMax))
        self.tMoteur = MoniteurProdCons(Tampon_fifo(tailleMax))
        self.tAss1 = MoniteurProdCons(Tampon_fifo(tailleMaxTamponsChaines))
        self.tAss2 = MoniteurProdCons(Tampon_fifo(tailleMaxTamponsChaines))
        self.tAss3 = MoniteurProdCons(Tampon_fifo(tailleMaxTamponsChaines))
        self.mutex = threading.Lock()
        self.CA1 = threading.Condition(self.mutex)
        self.CA2 = threading.Condition(self.mutex)
        self.CA3 = threading.Condition(self.mutex)

nbAvionsPrevus=5
#tailleMaxTamponsChaines=2
usine = UsineAeroplane()

def carlingue():
    for i in range(nbAvionsPrevus):
        time.sleep(random.randint(0, 3))
        tprint( 'Une carlingue est achevée ({})'.format(i+1))
        # A completer: deposer dans le tampon des carlingues
        moniteur_deposer(usine.tCarlingue,"carlingue",1)
        usine.CA1.notify()

def aile() :
    for i in range(nbAvionsPrevus*2):
        time.sleep(random.randint(0, 2))
        tprint( 'Une Aile est achevée ({})'.format(i+1))
        # A completer: deposer dans le tampon des ailes
        moniteur_deposer(usine.tAile,"aile",1)
        usine.CA1.notify()

def roue():
    for i in range(nbAvionsPrevus*3):
        time.sleep(random.randint(0, 2))
        tprint( 'Une roue est achevée ({})'.format(i+1))
        # A completer: deposer dans le tampon des roues
        moniteur_deposer(usine.tRoue,"roue",1)
        usine.CA2.notify()


def moteur():
    for i in range(nbAvionsPrevus*2):
        time.sleep(random.randint(0, 1))
        tprint( 'Un moteur est achevé ({})'.format(i+1))
        # A completer: deposer dans le tampon des moteurs
        moniteur_deposer(usine.tMoteur,"moteur",1)



def carlingue1Ailes2():
    for i in range(nbAvionsPrevus):
        # A completer: retirer 1 carlingue et 2 ailes des tampons
        while(tampon_nbElements(usine.tCarlingue) < 1 or tampon_nbElements(usine.tAile) < 2):
            usine.CA1.wait()
        usine.CA1.mutex.acquire()
        moniteur_retirer(usine.tCarlingue,"carlingue")
        moniteur_retirer(usine.tAile,"aile")
        moniteur_retirer(usine.tAile,"aile")
        time.sleep(random.randint(0, 3))
        tprint( 'Un assemblage 1 carlingue avec 2 ailes est achevé ({})'.format(i+1))
        # A completer: deposer dans le tampon des carlingue1Ailes2
        moniteur_deposer(usine.tAss1,"carlingue1Ailes2",1)
        usine.CA1.mutex.release()
        usine.CA2.notify()

def carlingue1Ailes2Roues3():
    for i in range(nbAvionsPrevus):
        while(tampon_nbElements(usine.tAss1) < 1 or tampon_nbElements(usine.tRoue) < 3):
            usine.CA2.wait()
        # A completer: retirer 1 carlingue1Ailes2 et 3 roues des tampons
        moniteur_retirer(usine.tAss1,"carlingue1Ailes2")
        moniteur_retirer(usine.tRoue,"roue")
        moniteur_retirer(usine.tRoue,"roue")
        moniteur_retirer(usine.tRoue,"roue")
        time.sleep(random.randint(0, 3))
        tprint( 'Un assemblage 1 carlingue et 2 ailes avec 3 roue est achevé ({})'.format(i+1))
        # A completer: deposer dans le tampon des carlingue1Ailes2Roues3
        moniteur_deposer(usine.tAss2,"carlingue1Ailes2Roues3",1)
        usine.CA3.notify()
        

def aeroplane():
    for i in range(nbAvionsPrevus):
        # A completer: retirer 1 carlingue1Ailes2Roues3 et 2 moteurs des tampons
        while(tampon_nbElements(usine.tMoteur) < 2 or tampon_nbElements(usine.tAss2) < 1):
            usine.CA3.wait()
        moniteur_retirer(usine.tAss2,"carlingue1Ailes2Roues3")
        moniteur_retirer(usine.tMoteur,"moteur")
        moniteur_retirer(usine.tMoteur,"moteur")
        time.sleep(random.randint(0, 3))
        tprint( 'Un aeroplane est achevé ({})'.format(i+1))
        # A completer: deposer dans le tampon des aeroplane
        moniteur_deposer(usine.tAss3,"aeroplane",1)
        

#
#  Test de l'usine d'assemblage d'aeroplanes
#

tprint('Demarrage de l\'usine')

# Création des Thread de chaine de production
threads=dict()
for chaine in [aile, roue, carlingue, moteur, carlingue1Ailes2, carlingue1Ailes2Roues3, aeroplane] :
    print( chaine.__name__ )
    threads[chaine]=threading.Thread(target=chaine)

# Démarrage des threads
for t in threads.values() :
    t.start()

# Attente de terminaison des threads
for t in threads.values() :
    t.join()

#tprint( 'Etat usine : ' + etat_usine ( usine ) )
tprint('Arret de l\'usine')

