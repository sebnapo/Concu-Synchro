#
#   Module pour problème des Producteurs Consommateurs
#   Definition du tampon LIFO et des fonctions d'accès:
#
#   - class Tampon_lifo( tailleMax )
#   - tampon_deposer ( tampon, element )
#   - tampon_retirer ( tampon ) -> element
#   - tampon_est_vide ( tampon )
#   - tampon_est_plein ( tampon )


import random
import time
#tprint = print
#from tprint import tprint

#  gestion du tampon 
class Tampon_lifo :
    def __init__ (self, tailleMax, dureeMax=2) :
        self.lifo = []              # liste LIFO 
        self.tailleMax= tailleMax   # Taille maximale du tampon 
        self.dureeMax= dureeMax     # duree maximale d'accès en secondes

def tampon_deposer( tampon, element ) :
    if tampon_est_plein(tampon) :
        tprint("Erreur Tampon Plein")
        return
    time.sleep(random.randint(0, tampon.dureeMax))
    tampon.lifo.append(element)
    
def tampon_retirer ( tampon ) :
    if tampon_est_vide( tampon ) :
        tprint("Erreur Tampon Vide")
        return
    time.sleep(random.randint(0, tampon.dureeMax))
    element=tampon.lifo.pop()
    return element

def tampon_est_vide ( tampon ) :
    return len(tampon.lifo) == 0

def tampon_est_plein (  tampon ) :
    return len(tampon.lifo) >= tampon.tailleMax

def tampon_nbElements (  tampon ) :
    return len(tampon.lifo)

# Exemple d'utilisation

def test_tampon():

    tampon = Tampon_lifo(2)

    print("Tampon plein=",tampon_est_plein(tampon))
    print("Tampon vide=",tampon_est_vide(tampon))
    tampon_deposer( tampon, 1 )
    tampon_deposer( tampon, 2 )
    print("Tampon plein=",tampon_est_plein(tampon))
    print("Tampon vide=",tampon_est_vide(tampon))
    tampon_retirer ( tampon )
    print("Tampon plein=",tampon_est_plein(tampon))
    print("Tampon vide=",tampon_est_vide(tampon))
    tampon_retirer ( tampon )
    print("Tampon plein=",tampon_est_plein(tampon))
    print("Tampon vide=",tampon_est_vide(tampon))
    tampon_deposer( tampon, 2 )
    print("Tampon plein=",tampon_est_plein(tampon))
    print("Tampon vide=",tampon_est_vide(tampon))
    tampon_retirer ( tampon )
    print("Tampon plein=",tampon_est_plein(tampon))
    print("Tampon vide=",tampon_est_vide(tampon))
    print("Fin du test")


if __name__ == "__main__" :
    test_tampon()
