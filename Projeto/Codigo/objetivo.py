from entidade import Entidade
from sprite import Sprite
import pygame

class Objetivo(Sprite, Entidade):

	def __init__(self, x, y, w, h, vel_x = 0, vel_y = 0, vel = 1, ativo = True, cor = (200, 0, 150), imagem=None):

		Entidade.__init__(self, x, y, w, h, vel_x, vel_y, vel)
		Sprite.__init__(self, imagem)

		self.__cor = cor
		self.__ativo = ativo

	def logica(self, jogador):

		if self.colidindo(jogador):
			self.__ativo = False

	def desenhar(self, superficie):

		if self.__ativo:

			if self.imagem:
				superficie.blit(self.imagem, (self.x, self.y))
			else:
				pygame.draw.rect(superficie, self.__cor, (self.x, self.y, \
											 self.w, self.h))
	def get_ativo(self):
		return self.__ativo
