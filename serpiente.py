import pygame

class cubo(object):
	filas = 20
	a = 500
	def __init__(self, empieza, dirnx=1, dirny=0, color=(255,0,0)):
		self.pos = empieza
		self.dirnx = dirnx
		self.dirny = dirny
		self.color = color

	def mueve(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

	def dibuja(self, superficie, ojos=False):
		dis = self.a // self.filas
		i = self.pos[0]
		j = self.pos[1]
		pygame.draw.rect(superficie, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
		if ojos:
			centro = dis // 2
			radio = 3
			circulo_medio = (i*dis+centro-radio, j*dis+8)
			circulo_medio2 = (i*dis+dis-radio*2, j*dis+8)
			pygame.draw.circle(superficie, (0,0,0), circulo_medio, radio)
			pygame.draw.circle(superficie, (0,0,0), circulo_medio2, radio)