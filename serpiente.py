import pygame
import tkinter as tk
import random
from tkinter import messagebox

class cubo(object):
	filas = 20
	a = 500
	def __init__(self, empieza, dirnx=1, dirny=0, color=(255,0,0)):
		self.posición = empieza
		self.dirnx = dirnx
		self.dirny = dirny
		self.color = color

	def mover(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.posición = (self.posición[0] + self.dirnx, self.posición[1] + self.dirny)

	def dibujar(self, superficie, ojos=False):
		distancia = self.a // self.filas
		i = self.posición[0]
		j = self.posición[1]
		pygame.draw.rect(superficie, self.color, (i*distancia+1, j*distancia+1, distancia-2, distancia-2))
		if ojos:
			centro = distancia // 2
			radio = 3
			circulo_medio = (i*distancia+centro-radio, j*distancia+8)
			circulo_medio2 = (i*distancia+distancia-radio*2, j*distancia+8)
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
					self.turnos[self.cabeza.posición[:]] = [self.dirnx, self.dirny]
				elif teclas[pygame.K_RIGHT]:
					self.dirnx = 1
					self.dirny = 0
					self.turnos[self.cabeza.posición[:]] = [self.dirnx, self.dirny]
				elif teclas[pygame.K_UP]:
					self.dirnx = 0
					self.dirny = -1
					self.turnos[self.cabeza.posición[:]] = [self.dirnx, self.dirny]
				elif teclas[pygame.K_DOWN]:
					self.dirnx = 0
					self.dirny = 1
					self.turnos[self.cabeza.posición[:]] = [self.dirnx, self.dirny]
		for i, c in enumerate(self.cuerpo):
			p = c.posición[:]
			if p in self.turnos:
				turno = self.turnos[p]
				c.mover(turno[0], turno[1])
				if i == len(self.cuerpo)-1:
					self.turnos.pop(p)
			else:
				if c.dirnx == -1 and c.posición[0] <= 0:
					c.posición = (c.filas-1, c.posición[1])
				elif c.dirnx == 1 and c.posición[0] >= c.filas-1:
					c.posición = (0, c.posición[1])
				elif c.dirny == 1 and c.posición[1] >= c.filas-1:
					c.posición = (c.posición[0], 0)
				elif c.dirny == -1 and c.posición[1] <= 0:
					c.posición = (c.posición[0], c.filas-1)
				else:
					c.mover(c.dirnx, c.dirny)

	def reposicionamiento(self, pos):
		self.cabeza = cubo(pos)
		self.cuerpo = []
		self.cuerpo.append(self.cabeza)
		self.turnos = {}
		self.dirnx = 0
		self.dirny = 1

	def crecer(self):
		cola = self.cuerpo[-1]
		dx, dy = cola.dirnx, cola.dirny
		if dx == 1 and dy == 0:
			self.cuerpo.append(cubo((cola.posición[0]-1,cola.posición[1])))
		elif dx == -1 and dy == 0:
			self.cuerpo.append(cubo((cola.posición[0]+1,cola.posición[1])))
		elif dx == 0 and dy == 1:
			self.cuerpo.append(cubo((cola.posición[0],cola.posición[1]-1)))
		elif dx == 0 and dy == -1:
			self.cuerpo.append(cubo((cola.posición[0],cola.posición[1]+1)))
		self.cuerpo[-1].dirnx = dx
		self.cuerpo[-1].dirny = dy

	def dibujar(self, superficie):
		for i, c in enumerate(self.cuerpo):
			if i == 0:
				c.dibujar(superficie, True)
			else:
				c.dibujar(superficie)

def dibujar_reja(a, filas, superficie):
	tamaño_entre = a // filas
	x = 0
	y = 0
	for l in range(filas):
		x = x + tamaño_entre
		y = y + tamaño_entre
		pygame.draw.line(superficie, (255,255,255), (x,0), (x,a))
		pygame.draw.line(superficie, (255,255,255), (0,y), (a,y))

def dibuja_ventana(superficie):
	global filas, ancho, serpiente, fruta
	superficie.fill((0,0,0))
	serpiente.dibujar(superficie)
	fruta.dibujar(superficie)
	dibujar_reja(ancho, filas, superficie)
	pygame.display.update()

def poner_fruta(filas, item):
	posición = item.cuerpo
	while True:
		x = random.randrange(filas)
		y = random.randrange(filas)
		if len(list(filter(lambda x:x.posición == (x,y), posición))) > 0:
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

def principal():
	global ancho, filas, serpiente, fruta
	ancho = 500
	filas = 20
	ventana = pygame.display.set_mode((ancho, ancho))
	serpiente = serpiente((255,0,0), (10,10))
	fruta = cubo(poner_fruta(filas, serpiente), color=(0,255,0))
	reloj = pygame.time.Clock()
	en_juego = True
	while en_juego:
		pygame.time.delay(50)
		reloj.tick(10)
		serpiente.mueve()
		if serpiente.cuerpo[0].posición == fruta.posición:
			serpiente.crecer()
			fruta = cubo(poner_fruta(filas, serpiente), color=(0,255,0))
		if serpiente.cuerpo[0].posición in list(map(lambda x:x.posición,serpiente.cuerpo[1:])):
			print("Puntuación: ", len(serpiente.cuerpo))
			caja_mensaje("¡Perdiste!", "¿Nuevo intento...?")
			serpiente.reposicionamiento((10,10))
		dibuja_ventana(ventana)

principal()