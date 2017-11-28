# -*- coding: utf8 -*-
import multiprocessing
import threading
import time
import random
tprint = print
# A d�commenter pour synchroniser l'affichage tprint()
#from tprint import tprint

#
# Impl�mentation d'un sémaphore de comptage à partir des moniteurs python (Lock et Condition)
#


#
# Définition du Moniteur sémaphore
#

class Semaphore_moniteur():
    def __init__(self,counter=0):
        # Variables d'état
        # A compléter: compteur (ressource critique)
        self.cpt = counter
        # A compléter: condition, mutex
        self.mutex = threading.Lock()
        self.condition = threading.Condition(self.mutex)
    
# Les Points d'entrée :

def P(semaphore):
    # A compléter : EM
    semaphore.mutex.acquire()
    # A compléter: décrémenter le compteur
    semaphore.cpt -= 1
    # A compléter: endormir si compteur < 0
    if(semaphore.cpt < 0) : semaphore.condition.wait()
    # A compléter : EM
    semaphore.mutex.release()

def V(semaphore):
    # A compléter : EM
    semaphore.mutex.acquire()
    # A compléter: incrémenter le compteur
    semaphore.cpt += 1
    # A compléter: reveiller processus endormi si compteur <= 0
    if(semaphore.cpt <= 0) : semaphore.condition.notify()
    # A compléter : EM
    semaphore.mutex.release()



# fin de definition du moniteur





#
# test 1 avec exlusion mutuelle par sémaphore
#
def testEM():


    # boucle de répétition de chaque thread
    NbCoups = 10

    # ressource critique:
    global RC
    RC = 0

    # Les semaphores
    semaphore = Semaphore_moniteur(1)



    # Threads P1
    def thread_P1(nom) :
        global RC
        tprint( '{nom} : Debut du thread nom={nom}'.format(nom=nom, pid=multiprocessing.current_process().pid, tid=threading.get_ident()))

        for i in range(NbCoups):
            time.sleep(random.randint(0, 3))

            # prise d'un jeton dans le semaphore
            tprint( '{nom} : Demande P(semaphore)'.format(nom=nom) )
            P(semaphore)

            # Debut de section critique
            tprint( '{nom} : Debut de section critique'.format(nom=nom))

            a = RC
            time.sleep(random.randint(0, 3))
            RC = a + 1
            tprint( '{nom} : \t (i={i}) RC={RC}'.format(nom=nom, i=i, RC=RC) )

            tprint( '{nom} : Fin de section critique'.format(nom=nom))
            # fin de section critique

            # liberation d'un jeton dans le semaphore pong (resp. ping)
            V(semaphore)
            tprint( '{nom} : V(semaphore)'.format(nom=nom) )
                
        tprint( '{nom} : Fin du thread'.format(nom=nom))

    # Threads P2
    def thread_P2(nom) :
        global RC
        tprint( '{nom} : Debut du thread nom={nom}'.format(nom=nom, pid=multiprocessing.current_process().pid, tid=threading.get_ident()))

        for i in range(NbCoups):
            time.sleep(random.randint(0, 3))

            # prise d'un jeton dans le semaphore
            tprint( '{nom} : Demande P(semaphore)'.format(nom=nom) )
            P(semaphore)

            # Debut de section critique
            tprint( '{nom} : Debut de section critique'.format(nom=nom))

            b = RC
            time.sleep(random.randint(0, 3))
            RC = b + 2
            tprint( '{nom} : \t (i={i}) RC={RC}'.format(nom=nom, i=i, RC=RC) )

            tprint( '{nom} : Fin de section critique'.format(nom=nom))
            # fin de section critique

            # liberation d'un jeton dans le semaphore pong (resp. ping)
            V(semaphore)
            tprint( '{nom} : V(semaphore)'.format(nom=nom) )
                
        tprint( '{nom} : Fin du thread'.format(nom=nom))



      
    # Création des Thread
##    P1 = threading.Thread(target=thread_P1, args=("P1",))
##    P2 = threading.Thread(target=thread_P2, args=("P2",))
##
##    tprint('Debut du test')
##
##    # Démarrage des threads
##    for t in [P1, P2]:
##        t.start()
##
##    # Attente de terminaison des threads
##    for t in [P1,P2]:
##        t.join()
##
##    tprint('Fin du test')



# Test 1 : Exemple de trace d'�x�cution (chronogramme)

#
# on obtient
#
#: Processus  :: Moniteur   :: Mutex   :: Variables   :Condition:
#:PE:P1::PE:P2::MP:MPE:MF   ::Mu:MuF   ::RC:i1:i2::C  : CA  :NA:: Comment
#:  :  ::  :  ::  :   :     ::1 :      ::0 :0 :0 ::1  :     :0 ::
#:P :L*::  :  ::  :   :     ::0 :      ::0 :0 :0 ::1  :     :0 ::P1 debut P(S), lock(Mu)>
#:P :*L::  :  ::P1:P  :     ::0 :      ::0 :0 :0 ::1  :     :0 ::P1 lock(Mu)<
#:P :  ::P :L*::P1:P  :     ::-1:P2    ::0 :0 :0 ::1  :     :0 ::P2 debut P(S), lock(Mu)>
#:P :  ::P :L ::P1:P  :P2   ::-1:P2    ::0 :0 :0 ::1  :     :0 ::P2 attend sur Mu
#:P :C-::P :L ::P1:P  :P2   ::-1:P2    ::0 :0 :0 ::0  :     :0 ::P1 C--
#:P :U ::P :L*::P1:P  :P2   ::0 :      ::0 :0 :0 ::0  :     :0 ::P1 unlock(Mu)->reveil P2
#:P :  ::P :  ::  :   :P2   ::0 :      ::0 :0 :0 ::0  :     :0 ::P1 fin P(S)
#:  :  ::P :*L::P2:P  :     ::0 :      ::0 :0 :0 ::0  :     :0 ::P2 lock(Mu)<, P2 reprend
# A COMPLETER ...

#
# Avec :
# Processus={P1,P2}
# PE: nom du point d'entr�e (P ou V)
# MP: Processus en cours dans le moniteur (th�orique)
# MPE: nom du point d'entr?e en cours dans le moniteur (th�orique) (P ou V)
# MF: Liste d'attente en entr�e du moniteur (th�orique)
# Mu: valeur du Mutex d'acc?s au moniteur(acc�s r�el)
# MuF: liste d'attente du Mutex d'acc?s au moniteur(acc�s r�el)
# CA: condition/liste attente "semaphore",
# C: compteur du "semaphore",
# RC: la ressource critique 
# NA: nombre de processus en attente sur CA (inutile)



#
# test 2 avec alternance Ping Pong avec sémaphores
#
def testAlternance():
    # liste des noms de threads à créer
    NomsThreads = ["PONG","PING"]
    # puis essayez avec:
    # NomsThreads = ["PONG","PING","PING","PONG","PING","PONG","PONG","PING"]
    threads = []

    # boucle de répétition de chaque thread
    NbCoups = 10

    # ressource critique:
    global chaine_ping_pong
    chaine_ping_pong = ''

    # Les semaphores
    semaphore_ping = Semaphore_moniteur(1)
    semaphore_pong = Semaphore_moniteur(0)



    # Threads de type Ping (resp. Pong)
    def thread_ping_pong(nom) :
        global chaine_ping_pong
        tprint( '{nom} : Debut du thread nom={nom}, pid={pid}, tid={tid}'.format(nom=nom, pid=multiprocessing.current_process().pid, tid=threading.get_ident()))

        for i in range(NbCoups):
            time.sleep(random.randint(0, 3))

            # prise d'un jeton dans le semaphore ping (resp. pong)
            tprint( '{nom} : Demande P(semaphore_{noml})'.format(nom=nom, noml=nom.lower()) )
            if nom is "PING" :
                semaphore=semaphore_ping
            else :
                semaphore=semaphore_pong
            P(semaphore)

            # Debut de section critique
            tprint( '{nom} : Debut de section critique'.format(nom=nom))

            time.sleep(random.randint(0, 3))
            chaine_ping_pong = chaine_ping_pong + nom + ' '
            tprint( '{nom} : \t (i={i}) chaine_ping_pong={chaine_ping_pong}'.format(nom=nom, i=i, chaine_ping_pong=chaine_ping_pong) )

            tprint( '{nom} : Fin de section critique'.format(nom=nom))
            # fin de section critique

            # liberation d'un jeton dans le semaphore pong (resp. ping)
            if nom is "PING" :
                semaphore=semaphore_pong
            else :
                semaphore=semaphore_ping
            V(semaphore)
            tprint( '{nom} : V(semaphore_{noml})'.format(nom=nom, noml=nom.lower()) )
                
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







if __name__ == "__main__" :
    testEM()
    testAlternance()
