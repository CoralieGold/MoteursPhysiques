# -*- coding: utf-8 -*-
from math       import sqrt
from tkGraphPad import *
from geom       import *

#___________________ GLOBALS ___________________________#
EPSILON = 0.00000001
RAYON = 0.1

#___________________ UTILS _____________________________#
def distPM(M1,M2) :
	return distance(M1.pos,M2.pos)

# __________________ COLLISIONS ________________________#

def detectCollisions(M):
	col = False
	if((M.pos.y + M.h) < 0):
		M.pos.y = 0
		M.v.y = - M.v.y
		col = True
		
	if((M.pos.y + M.h) > 5):
		M.pos.y = 5
		M.v.y = - M.v.y
		col = True
		
	if((M.pos.x + M.h) < 0):
		M.pos.x = 0
		M.v.x = - M.v.x
		col = True
	
	if((M.pos.x + M.h) > 10):
		M.pos.x = 10
		M.v.x = - M.v.x
		col = True

#____________________ CLASSES __________________________#

# PARTICULES

class PMat():
	# masse, position, vitesse, acceleration, couleur, rayon
	def __init__(self, m, pos, v, a, h=0, color="red", ray=RAYON):
		self.m = m
		self.pos = pos
		self.v = v
		self.a = a
		self.color = color
		self.ray = ray
		self.h = h

	def draw(self):
		win.graphpad.fillcircle(self.pos, self.ray, self.color)
		
		
class PointFixe(PMat):
	def __init__(self, pos, color="red", ray=RAYON):
		PMat.__init__(self, 0.005, pos, 0, 0, 0, color, ray)
		self.frc = Vecteur(0,0)

class Particule(PMat):
	def __init__(self, m, pos, v, a, h=0, color="red", ray=RAYON):
		PMat.__init__(self, m, pos, v, a, h, color, ray)
		self.frc = Vecteur(0, 0)
		
	def setup(self) :
		self.v += (self.h / self.m) * self.frc
		self.pos += self.h * self.v
		self.frc = Vecteur(0,0)
	

# LIAISONS

'''class Link():
	
	# longueur, raideur, dissipation energie, seuil
	def __init__(self, l, k, z, s):
		self.l = l
		self.k = k
		self.z = z
		self.s = s'''

class Liaison():
	def __init__(self, M1, M2, color):
		self.M1 = M1
		self.M2 = M2
		self.frc = Vecteur(0., 0.)
		self.color = color
		if M1 != None and M2 != None:
			self.l = distPM(M1, M2)
		
	def setup(self):
		if self.M1: self.M1.frc += self.frc
		if self.M2: self.M2.frc -= self.frc
		
	def draw(self): 
		if self.color == None : return
		line(self.M1.pos, self.M2.pos, self.color, 1)

class Ressort(Liaison) :
	def __init__(self, M1, M2, k, color=None):
		Liaison.__init__(self, M1, M2, color)
		self.k = k

	def setup(self):
		global EPSILON
		d = max(EPSILON, distPM(self.M1, self.M2)) 
		e = (1. - self.l / d)

		self.frc = self.k * e * (Vecteur(self.M1.pos, self.M2.pos))
		Liaison.setup(self)
'''
class ParticlesSystem(Liaison) :
	def __init__(self, M1, M2, k, color=None):
		Liaison.__init__(self, M1, M2, color)
		self.k = k

	def setup(self):
		global EPSILON
		d = max(EPSILON, distPM(self.M1, self.M2)) 
		if(d <= 2*RAYON):
			print("collision", self.M1.color, self.M2.color)
			e = (1. - 2 * RAYON / d)

			self.frc = self.k * e * (Vecteur(self.M1.pos, self.M2.pos))
			Liaison.setup(self)
'''

class Gravite(Liaison) :
	def __init__(self, M, frc):
		Liaison.__init__(self, M, None, None)
		self.frc = frc
	 
	def setup(self):
		Liaison.setup(self)

#____________________FONCTIONS       ____________________#

#==========================
# Modeleur : Construction -- "statique"
def Modeleur() :
	''' '''
	points = []
	points.append(PointFixe(pos=Point(1, 2.5), color="grey"))
	points.append(Particule(m=1, pos=Point(2, 2.5), v=Vecteur(0, 0), a=0, h=0.001, color="red"))
	points.append(Particule(m=1, pos=Point(3, 2.5), v=Vecteur(0, 0), a=0, h=0.001, color="blue"))
	points.append(Particule(m=1, pos=Point(4, 2.5), v=Vecteur(0, 0), a=0, h=0.001, color="green"))
	points.append(PointFixe(pos=Point(5, 2.5), color="purple"))
	points.append(Particule(m=1, pos=Point(6, 2.5), v=Vecteur(0, 0), a=0, h=0.001, color="turquoise"))
	points.append(Particule(m=1, pos=Point(7, 2.5), v=Vecteur(0, 0), a=0, h=0.001, color="yellow"))
	points.append(Particule(m=1, pos=Point(8, 2.5), v=Vecteur(0, 0), a=0, h=0.001, color="black"))
	points.append(PointFixe(pos=Point(9, 2.5), color="orange"))
	
	liaisons = []

	for i in range(len(points) - 1):
		liaisons.append(Ressort(points[i], points[i+1], k=50000, color="blue"))
	for p in points:
		liaisons.append(Gravite(p, G))

	return points, liaisons
    
#==========================
# fonction animatrice
def anim():
	"""fonction animatrice""" 
   
	for p in points:
		if isinstance(p, Particule):
			p.setup()
			detectCollisions(p)
    
	for l in liaisons:
		l.setup()

      
#==========================
# fonction de dessin
def draw():
  """fonction de dessin"""
  win.clear() # nettoyage
    
  # Draw points
  for p in points:
    p.draw()
    
  for l in liaisons:
    l.draw()

#____________________PRINCIPAL       ____________________#
if __name__ == '__main__':
#==========================

  # Démarrage du réceptionnaire d'evenements :
  win=MainWindow("TP3",900,450,"lightgrey")
  win.SetDrawZone(0,0,+10,+5)

  g = 10
  G = Vecteur(0, -g)
   
  points, liaisons = Modeleur()    
  
  win.anim=anim  
  win.draw=draw
  win.startmainloop()
