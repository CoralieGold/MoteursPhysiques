# -*- coding: utf-8 -*-
from math       import sqrt
from tkGraphPad import MainWindow


#____________________FONCTIONS       ____________________#

#==========================
# Modeleur : Construction -- "statique"
def Modeleur() :
  ''' '''
  pass
    
#==========================
# fonction animatrice
def anim():
  """fonction animatrice"""
  pass
        
#==========================
# fonction de dessin
def draw():
  """fonction de dessin"""
  win.clear() # nettoyage
  dt=dtscale.get() 
  
  pass

#____________________PRINCIPAL       ____________________#
if __name__ == '__main__':
#==========================

  # Démarrage du réceptionnaire d'evenements :
  win=MainWindow("Corde 1D",900,450,"lightgrey")
  win.SetDrawZone(-6,-3,+6,+3)
      
  dt=0.1
  Modeleur()    
  
  # scrollbars
  dtscale=win.CreateScalev(label='dt',inf=0,sup=1,step=0.01)
  dtscale.set(dt)

  win.anim=anim  
  win.draw=draw
  win.startmainloop()

