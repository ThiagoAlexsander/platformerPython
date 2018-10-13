import pygame
from entidade import Entidade
from sprite import Sprite

class Jogador(Entidade, Sprite):

	def __init__(self, x, y, w, h, vel_x, vel_y, vel, cor = (0, 25, 125), imagem=None):

		Entidade.__init__(self, x, y, w, h, vel_x, vel_y, vel)
		Sprite.__init__(self, imagem, cor)

		self.__vida = 1
		self.__gravidade = 5.8 #3.2
		self.__cor = cor
		self.__no_chao = False
		self.x_inicial = x
		self.y_inicial = y

	def clonar(self):

		return Jogador(self.x, self.y, self.w, self.h, self.vel_x, self.vel_y, self.vel, self.cor, self.caminho_imagem)

	#def resetar(self):

	#	self.__vida = 3

	def reposicionar(self):
		self.vel_x = 0
		self.vel_y = 0
		self.x = self.x_inicial
		self.y = self.y_inicial

	def desenhar(self, superficie, pos):

		if not self.imagem:
			self.inicializar()

		#superficie.blit(self.imagem, (self.x, self.y))
		
		superficie.blit(self.imagem, pos)

	def __pular(self, ents):
		
		if self.__no_chao:

			self.vel_y = -400 #-240 #-350
			self.__no_chao = False

	def __evento(self, ents):
		e = pygame.key.get_pressed() # Pega os eventos.
		
		if e[pygame.K_LEFT]:
			self.vel_x -= self.vel

		elif e[pygame.K_RIGHT]:
			self.vel_x += self.vel
		
		if e[pygame.K_UP]:
			if self.__no_chao:
				self.__pular(ents)

	def logica(self, dt, ents):

		self.__evento(ents)
		for ent in ents:

			if self.colidindo_cima(ent):

				if self.y + self.h > ent.y:
					self.__no_chao = True
					
					if str(ent) == "vertical":
						self.vel_y = ent.vel_y
						dt = 1
					else:
						self.vel_y = -self.__gravidade# - ent.vel_y
						self.vel_x += ent.vel_x

			elif self.vel_y > -self.__gravidade and dt != 1:
				self.__no_chao = False
				
			if self.colidindo_baixo(ent):

				if self.y < ent.y + ent.h:

					if str(ent) == "vertical":						
						self.vel_y = -self.vel_y - ent.vel_y
					else:
						self.vel_y = 0

			if self.colidindo_esquerda(ent):
				self.vel_x = ent.vel_x - ent.vel

			if self.colidindo_direita(ent):
				self.vel_x = ent.vel_x + ent.vel
				
		if dt != 1:
			self.vel_y += self.__gravidade

		#if self.vel_y > 400.0: # Limita a velocidade para evitar bugs.
		#	self.vel_y = 390.0

		self.x += self.vel_x
		self.y += self.vel_y * dt

		self.vel_x = 0

	def adicionar_vida(self):
		self.__vida += 1

	def subtrair_vida(self):
		self.__vida -= 1

	def get_no_chao(self):
		return self.__no_chao

	def get_vida(self):
		return self.__vida

	def set_vida(self, vida):
		self.__vida = vida

	def get_cor(self):
		return self.__cor