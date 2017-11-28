#
#   Module pour problème des Producteurs Consommateurs
#   Definition du tampon fifo et des fonctions d'accès:
#
#   - class Tampon_fifo( tailleMax )
#   - tampon_deposer ( tampon, element )
#   - tampon_retirer ( tampon ) -> element
#   - tampon_est_vide ( tampon )
#   - tampon_est_plein ( tampon )


import random
import time
#tprint = print
from tprint import tprint

#  gestion du tampon 
class Tampon_fifo :
    def __init__ (self, tailleMax, dureeMax=2) :
        self.fifo = []              # liste FIFO 
        self.tailleMax= tailleMax   # Taille maximale du tampon 
        self.dureeMax= dureeMax     # duree maximale d'accès en secondes

def tampon_deposer( tampon, element ) :
    if tampon_est_plein(tampon) :
        tprint("Erreur Tampon Plein")
        return
    time.sleep(random.randint(0, tampon.dureeMax))
    tampon.fifo.append(element)
    
def tampon_retirer ( tampon ) :
    if tampon_est_vide( tampon ) :
        tprint("Erreur Tampon Vide")
        return
    time.sleep(random.randint(0, tampon.dureeMax))
    element=tampon.fifo[0]
    tampon.fifo=tampon.fifo[1:]
    return element

def tampon_est_vide ( tampon ) :
    return len(tampon.fifo) == 0

def tampon_est_plein (  tampon ) :
    return len(tampon.fifo) >= tampon.tailleMax

def tampon_nbElements (  tampon ) :
    return len(tampon.fifo)

# Exemple d'utilisation

def test_tampon():

    tampon = Tampon_fifo(2)

    print("Tampon=", tampon.fifo)
    print("Tampon plein=",tampon_est_plein(tampon))
    print("Tampon vide=",tampon_est_vide(tampon))

    tampon_deposer( tampon, 1 )
    tampon_deposer( tampon, 2 )
    print("Tampon=", tampon.fifo)
    print("Tampon plein=",tampon_est_plein(tampon))
    print("Tampon vide=",tampon_est_vide(tampon))

    print("Retirer:", tampon_retirer ( tampon ))
    print("Tampon=", tampon.fifo)
    print("Tampon plein=",tampon_est_plein(tampon))
    print("Tampon vide=",tampon_est_vide(tampon))
    
    print("Retirer:", tampon_retirer ( tampon ))
    print("Tampon=", tampon.fifo)
    print("Tampon plein=",tampon_est_plein(tampon))
    print("Tampon vide=",tampon_est_vide(tampon))
    
    tampon_deposer( tampon, 3 )
    print("Tampon=", tampon.fifo)
    print("Tampon plein=",tampon_est_plein(tampon))
    print("Tampon vide=",tampon_est_vide(tampon))
    
    print("Retirer:", tampon_retirer ( tampon ))
    print("Tampon=", tampon.fifo)
    print("Tampon plein=",tampon_est_plein(tampon))
    print("Tampon vide=",tampon_est_vide(tampon))
    print("Fin du test")


if __name__ == "__main__" :
    test_tampon()
