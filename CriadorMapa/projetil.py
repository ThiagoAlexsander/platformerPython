from sprite import Sprite
from entidade import Entidade
import pygame

class Projetil(Entidade, Sprite):

	def __init__(self, x, y, w, h, vel_x, vel_y, vel, lado, cor, imagem):

		Entidade.__init__(self, x, y, w, h, vel_x, vel_y, vel)
		Sprite.__init__(self, imagem, cor)

		self.__cor = cor
		self.lado = lado		
		self.ativo = True

	def desenhar(self, superficie, pos):

		if not self.imagem:
			self.inicializar()
		
		#superficie.blit(self.imagem, (self.x, self.y))
		
		superficie.blit(self.imagem, pos)

	def logica(self, jogador):
		if self.colidindo(jogador):
			jogador.subtrair_vida()
			self.ativo = False
		elif (self.x > 800 or self.x < 0):
			self.ativo = False
		else:
			self.mover()

	def mover(self):

		if self.lado == 0:
			self.vel_x = -self.vel
		else:
			self.vel_x = self.vel

		#print(self.vel_x)

		self.x += self.vel_x
		#self.y += self.vel_y
		#print(self.x)