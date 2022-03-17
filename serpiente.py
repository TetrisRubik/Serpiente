import pygame
import tkinter as tk
import random
from tkinter import messagebox

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

class serpiente(object):
	cuerpo = []
	turnos = {}

	def __init__(self, color, pos):
		self.color = color
		self.cabeza = cubo(pos)
		self.cuerpo.append(self.cabeza)
		self.dirnx = 0
		self.dirny = 1

	def mueve(self):
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				pygame.quit()
			teclas = pygame.key.get_pressed()
			for tecla in teclas:
				if teclas[pygame.K_LEFT]:
					self.dirnx = -1
					self.dirny = 0
					self.turnos[self.cabeza.pos[:]] = [self.dirnx, self.dirny]
				elif teclas[pygame.K_RIGHT]:
					self.dirnx = 1
					self.dirny = 0
					self.turnos[self.cabeza.pos[:]] = [self.dirnx, self.dirny]
				elif teclas[pygame.K_UP]:
					self.dirnx = 0
					self.dirny = -1
					self.turnos[self.cabeza.pos[:]] = [self.dirnx, self.dirny]
				elif teclas[pygame.K_DOWN]:
					self.dirnx = 0
					self.dirny = 1
					self.turnos[self.cabeza.pos[:]] = [self.dirnx, self.dirny]
		for i, c in enumerate(self.cuerpo):
			p = c.pos[:]
			if p in self.turnos:
				turno = self.turnos[p]
				c.mueve(turno[0], turno[1])
				if i == len(self.cuerpo)-1:
					self.turnos.pop(p)
			else:
				if c.dirnx == -1 and c.pos[0] <= 0:
					c.pos = (c.filas-1, c.pos[1])
				elif c.dirnx == 1 and c.pos[0] >= c.filas-1:
					c.pos = (0, c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.filas-1:
					c.pos = (c.pos[0], 0)
				elif c.dirny == -1 and c.pos[1] <= 0:
					c.pos = (c.pos[0], c.filas-1)
				else:
					c.mueve(c.dirnx, c.dirny)

	def reposicionamiento(self, pos):
		self.cabeza = cubo(pos)
		self.cuerpo = []
		self.cuerpo.append(self.cabeza)
		self.turnos = {}
		self.dirnx = 0
		self.dirny = 1

	def añade_cubo(self):
		cola = self.cuerpo[-1]
		dx, dy = cola.dirnx, cola.dirny
		if dx == 1 and dy == 0:
			self.cuerpo.append(cubo((cola.pos[0]-1,cola.pos[1])))
		elif dx == -1 and dy == 0:
			self.cuerpo.append(cubo((cola.pos[0]+1,cola.pos[1])))
		elif dx == 0 and dy == 1:
			self.cuerpo.append(cubo((cola.pos[0],cola.pos[1]-1)))
		elif dx == 0 and dy == -1:
			self.cuerpo.append(cubo((cola.pos[0],cola.pos[1]+1)))
		self.cuerpo[-1].dirnx = dx
		self.cuerpo[-1].dirny = dy

	def dibuja(self, superficie):
		for i, c in enumerate(self.cuerpo):
			if i == 0:
				c.dibuja(superficie, True)
			else:
				c.dibuja(superficie)

def dibuja_reja(a, filas, superficie):
	tamaño_entre = a // filas
	x = 0
	y = 0
	for l in range(filas):
		x = x + tamaño_entre
		y = y + tamaño_entre
		pygame.draw.line(superficie, (255,255,255), (x,0), (x,a))
		pygame.draw.line(superficie, (255,255,255), (0,y), (a,y))

def dibuja_ventana(superficie):
	global filas, anchura, s, fruta
	superficie.fill((0,0,0))
	s.dibuja(superficie)
	fruta.dibuja(superficie)
	dibuja_reja(anchura, filas, superficie)
	pygame.display.update()

def pon_fruta(filas, item):
	pos = item.cuerpo
	while True:
		x = random.randrange(filas)
		y = random.randrange(filas)
		if len(list(filter(lambda z:z.pos == (x,y), pos))) > 0:
			continue
		else:
			break
	return (x,y)

def caja_mensaje(sujeto, contenido):
	raíz = tk.Tk()
	raíz.attributes("-topmost", True)
	raíz.withdraw()
	messagebox.showinfo(sujeto, contenido)
	try:
		raíz.destroy()
	except:
		pass