# -*- coding: utf-8 -*-
from math       import sqrt
from tkGraphPad import MainWindow
from geom       import Point, Vecteur

#____________________ CLASSES       ____________________#

class PMat():
	# masse, position, vitesse, acceleration, couleur, rayon
	def __init__(self, m, pos, v, a, color="red", ray=0.2):
		self.m = m
		self.pos = pos
		self.v = v
		self.a = a
		self.color = color
		self.ray = ray
		
	def eulerImp(self, h, G):
		self.v = (self.m / (self.m + h * alpha)) * (self.v - h*G)
		self.pos += h * self.v
		
	# alpha: coefficient de frottement dans l'air
	def eulerExp(self, h, G, alpha):
		self.pos += h * self.v
		self.v += (h / self.m) * self.a
		self.a = -G - (alpha / self.m) * self.v
		
		
class PointFixe(PMat):
	def __init__(self, pos, color="red", ray=0.2):
		PMat.__init__(self, 0.005, pos, 0, 0, color, ray)

class Particule(PMat):
	def __init__(self, m, pos, v, a, color="red", ray=0.2):
		PMat.__init__(self, m, pos, v, a, color, ray)
		
class Link():
	
	# longueur, raideur, dissipation energie, seuil
	def __init__(self, l, k, z, s):
		self.l = l
		self.k = k
		self.z = z
		self.s = s

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

  # Methode explicite
  p0.eulerExp(t0, G)
  
  # Methode implicite
  p1.eulerImp(t0, G)
  
  t0 += dt
        
#==========================
# fonction de dessin
def draw():
  """fonction de dessin"""
  win.clear() # nettoyage
  dt=dtscale.get() 
 
  t = 0
  p = Particule(1, Point(x0, z0), v0, Vecteur(0, 0))
  while(t < 1):
    win.graphpad.line(p.pos, Point(p.pos.x + p.v.x*t, p.pos.y + p.v.y*t - 0.5*g*t**2), "blue", 0.01)
    p.pos.x += p.v.x*t
    p.pos.y += p.v.y*t - 0.5*g*t**2
    p.v.y -= g*t
    t += dt
    
  win.graphpad.fillcircle(p0.pos, 0.2, "red")
  win.graphpad.fillcircle(p1.pos, 0.2, "green")

#____________________PRINCIPAL       ____________________#
if __name__ == '__main__':
#==========================

  # Démarrage du réceptionnaire d'evenements :
  win=MainWindow("TP1",900,450,"lightgrey")
  win.SetDrawZone(0,0,+10,+5)
      
  t0 = 0
  dt = 0.005
  g = 10
  x0 = 0
  z0 = 0.5
  v0 = Vecteur(5, 9)
  G = Vecteur(0, g)
  
  # Particule pour la méthode explicite
  p0 = Particule(1, Point(x0, z0), v0, -G)
  # Particule pour la méthode implicite
  p1 = Particule(1, Point(x0, z0), v0, -G)
  
  Modeleur()    
  
  # scrollbars
  dtscale=win.CreateScalev(label='dt',inf=0.01,sup=0.1,step=0.001)
  dtscale.set(dt)

  win.anim=anim  
  win.draw=draw
  win.startmainloop()
