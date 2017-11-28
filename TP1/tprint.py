import multiprocessing
import threading
import time
import datetime

#
#  Définition d'une fonction d'affichage protégée "tprint"
#       fonctionne en E.M.
#       préfixe les messages avec la date et le tid
#

mutex_tprint = threading.Lock()

def tprint(chaine) :
    global mutex_tprint
    pid=multiprocessing.current_process().pid
    tid=threading.get_ident()
    time=datetime.datetime.now().time()
    mutex_tprint.acquire()
    print('{time} : {tid} : {message}'.format(time=time, tid=tid, message=chaine))
    mutex_tprint.release()
