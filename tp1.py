# -*- coding: utf-8 -*-
from math       import sqrt
from tkGraphPad import MainWindow
from geom       import Point, Vecteur

#____________________ CLASSES       ____________________#

class PMat():
	# masse, position, vitesse, acceleration, couleur, rayon
	def __init__(self, m, pos, v, a, color="red", ray=0.1):
		self.m = m
		self.pos = pos
		self.v = v
		self.a = a
		self.color = color
		self.ray = ray
		
	def eulerImp(self, h, G, alpha):
		self.v = (self.m / (self.m + h * alpha)) * (self.v + h*G)
		self.pos += h * self.v
		
	# alpha: coefficient de frottement dans l'air
	def eulerExp(self, h, G, alpha):
		self.pos += h * self.v
		self.v += (h / self.m) * self.a
		# self.a = - G - (alpha / self.m) * self.v
	
	def leapFrog(self, h, G, alpha):
		self.v += (h / self.m) * self.a
		self.pos += h * self.v
		
		
class PointFixe(PMat):
	def __init__(self, pos, color="red", ray=0.1):
		PMat.__init__(self, 0.005, pos, 0, 0, color, ray)

class Particule(PMat):
	def __init__(self, m, pos, v, a, color="red", ray=0.1):
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
  global t0, p0, p1
  
  dt = dtscale.get() 
  alpha = alphascale.get()

  # Methode explicite : rouge
  p0.eulerExp(t0, G, alpha)
  
  # Methode implicite : vert
  p1.eulerImp(t0, G, alpha)
  
  # Methode leap frog : bleu
  p2.leapFrog(t0, G, alpha)
  
  t0 += dt

        
#==========================
# fonction de dessin
def draw():
  """fonction de dessin"""
  win.clear() # nettoyage
  dt=dtscale.get() 
  
  global p0, p1
   
  t = 0
  pA = Point(x0, z0)
  pB = Point(x0, z0)
  vA = Vecteur(5, 9)
  vB = Vecteur(5, 9)

  while(t < 0.5):
    pB.x += vA.x * t
    pB.y += vA.y * t - 0.5 * g * t**2
    vB.y -= g*t
    
    win.graphpad.line(pA, pB, "blue", 0.01)

    pA.x = pB.x
    pA.y = pB.y
    vA.y = vB.y
    
    t += dt
    
  win.graphpad.fillcircle(p0.pos, 0.1, p0.color)
  win.graphpad.fillcircle(p1.pos, 0.1, p1.color)
  win.graphpad.fillcircle(p2.pos, 0.1, p2.color)

#____________________PRINCIPAL       ____________________#
if __name__ == '__main__':
#==========================

  # Démarrage du réceptionnaire d'evenements :
  win=MainWindow("TP1",900,450,"lightgrey")
  win.SetDrawZone(0,0,+10,+5)
      
  t0 = 0
  dt = 0.00005
  g = 10
  x0 = 0
  z0 = 0.5
  G = Vecteur(0, -g)
  alpha = 0.005
  
  # Particule pour la méthode explicite
  p0 = Particule(1, Point(x0, z0), Vecteur(5, 9), Vecteur(0, -g), color="red")
  # Particule pour la méthode implicite
  p1 = Particule(1, Point(x0, z0), Vecteur(5, 9), Vecteur(0, -g), color="green")
  # Particule pour la méthode leap frog
  p2 = Particule(1, Point(x0, z0), Vecteur(5, 9), Vecteur(0, -g), color="blue")
  
  Modeleur()    
  
  # scrollbars
  dtscale=win.CreateScalev(label='dt',inf=0.00001,sup=0.1,step=0.0001)
  dtscale.set(dt)
  
  alphascale=win.CreateScalev(label='alpha',inf=0.001,sup=1,step=0.01)
  alphascale.set(alpha)

  win.anim=anim  
  win.draw=draw
  win.startmainloop()
