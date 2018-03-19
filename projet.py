# -*- coding: utf-8 -*-
from math       import sqrt
from tkGraphPad import *
from geom       import *
import random

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

class ParticlesSystem(Liaison) :
	def __init__(self, M1, M2, k, color=None):
		Liaison.__init__(self, M1, M2, color)
		self.k = k

	def setup(self):
		global EPSILON
		d = max(EPSILON, distPM(self.M1, self.M2)) 
		if(d <= 2*self.M2.ray):
			self.l = self.M2.ray/2
			e = (1. - self.l / d)

			self.frc = -self.k * e * (Vecteur(self.M1.pos, self.M2.pos))
			Liaison.setup(self)

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

	particules = []
	for i in range(60):
		x = random.uniform(2*RAYON, maxX-2*RAYON)
		vX = random.uniform(0.5, 2)
		vY = random.uniform(0.5, 2)
		particules.append(Particule(m=1, pos=Point(x, maxY/2), v=Vecteur(vX, vY), a=0, h=0.001, color=random.choice(colors)))
	
	points = []
	points.extend(particules)
	
	liaisons = []
	for p1 in particules:
		for p2 in points:
			liaisons.append(ParticlesSystem(p1, p2, k=5000, color=None))
		
		liaisons.append(Gravite(p1, G))
		

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
  win=MainWindow("TP4",900,450,"black")
  
  maxX = 10
  maxY = 5
  win.SetDrawZone(0,0,maxX,maxY)

  g = 10
  G = Vecteur(0, -g)
  #colors = ('red', 'green', 'blue', 'yellow', 'magenta', 'cyan')
  colors = ('aliceblue', 'aquamarine', 'cadetblue', 'cornflowerblue', 'snow',
			'darkcyan', 'dodgerblue', 'deepskyblue', 'lightblue', 'lightcyan',
			'mediumturquoise', 'royalblue', 'skyblue', 'steelblue', 'turquoise',
			'teal', 'silver', 'powderblue', 'paleturquoise', 'mintcream', 
			'mediumaquamarine', 'lightsteelblue', 'lightskyblue')
  
  
  points, liaisons = Modeleur()    
  
  win.anim=anim  
  win.draw=draw
  win.startmainloop()
