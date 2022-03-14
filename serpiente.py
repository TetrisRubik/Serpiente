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