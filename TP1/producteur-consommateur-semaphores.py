import threading
import tampon_lifo
tprint = print
# A décommenter pour synchroniser l'affichage tprint()
from tprint import tprint

#
#   Problème des "Producteurs Consommateurs"
#   Solution à l'aide de sémaphores
#


#
# Ressources critiques
#
# Tampon
tailleMaxTampon = 2
tampon = tampon_lifo.Tampon_lifo(tailleMaxTampon)

# Sémaphores
Sp = threading.Semaphore(tailleMaxTampon)
Sc = threading.Semaphore(0)
S = threading.Semaphore(1)

#
# Threads Producteurs et Consommateurs
#

# Fonction principales des threads "producteurs" 
def producteur(nom)  :

    element=nom[1:]
 
    Sp.acquire()
    S.acquire()
    # code en E.M. sur mutex
    tprint("        {nom} depose \"{element}\" dans le tampon...".format(nom=nom, element=element))
    tampon_lifo.tampon_deposer(tampon, element)
    tprint("        {nom} a fini de deposee \"{element}\" dans le tampon...".format(nom=nom, element=element))
    #tprint("        {nom} tampon = {tampon}".format(nom=nom, tampon=tampon.lifo))
    # fin d'E.M.
    Sc.release()
    S.release()


# Fonction principales des threads "consommateurs" 
def consommateur(nom)  :

    Sc.acquire()
    S.acquire()

    # code en E.M. sur mutex
    tprint("        {nom} retire un element du tampon...".format(nom=nom))
    element = tampon_lifo.tampon_retirer(tampon)
    tprint("        {nom} a fini de retirer \"{element}\" du tampon...".format(nom=nom, element=element))
    #tprint("        {nom} tampon = {tampon}".format(nom=nom, tampon=tampon.lifo))
    # fin d'E.M.
    Sp.release()
    S.release()
    
    return element



# Exemple d'utilisation

def test_prod_cons_avec_semaphores():


    # Fonction principales de création et de démarrage des threads 
    nomsThreads  =  ["c1","p1", "p2", "p3", "p4", "c2", "c3", "c4 "]
    threads = []

    for nomT in nomsThreads  :
        if nomT[0]=='p' :
            thread_main = producteur
        else :
           thread_main = consommateur
        threads.append( threading.Thread(target=thread_main, name=nomT, args=(nomT,)))

    tprint("Debut du test")
    
    for t in threads :  
        t.start()
        tprint("{name} demarre".format(name=t.name))

    for t in threads :
        t.join()
        tprint("{name} est terminé".format(name=t.name))

    tprint("Fin du test")



if __name__ == "__main__" :
    test_prod_cons_avec_semaphores()



