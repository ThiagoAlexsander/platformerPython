from entidade import Entidade
from sprite import Sprite
import pygame

class Energia(Sprite, Entidade):

	def __init__(self, x, y, w, h, vel_x = 0, vel_y = 0, vel = 1, ativo = True, cor = (200, 0, 150), imagem = None):

		Entidade.__init__(self, x, y, w, h, vel_x, vel_y, vel)
		Sprite.__init__(self, imagem, cor)
		self.__ativo = ativo

	def clonar(self):
		return Energia(self.x, self.y, self.w, self.h, self.vel_x, self.vel_y, self.vel, self.__ativo, self.cor, self.caminho_imagem)

	def resetar(self):
		self.__ativo = True

	def logica(self, jogador):

		if self.colidindo(jogador):
			self.__ativo = False

	def desenhar(self, superficie, pos):

		if self.__ativo:

			if not self.imagem:
				self.inicializar()

			#superficie.blit(self.imagem, (self.x, self.y))
			superficie.blit(self.imagem, pos)
				
	def get_ativo(self):
		return self.__ativo