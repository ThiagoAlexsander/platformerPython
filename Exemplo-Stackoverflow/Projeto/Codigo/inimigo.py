from arma import Arma
from entidade import Entidade
from sprite import Sprite
import pygame

class Inimigo(Entidade, Sprite, Arma):

	def __init__(self, x, y, w, h, vel_x, vel_y, vel, ativo = True, intervalo = 3.0, lado = 0, cor = (0, 25, 125), imagem = None, imagem_bala = None):

		Entidade.__init__(self, x, y, w, h, vel_x, vel_y, vel)
		Sprite.__init__(self, imagem, cor)
		Arma.__init__(self, ativo, intervalo, lado)

		self.__cor = cor
		self.__intervalo_original = intervalo
		self.__imagem_bala = imagem_bala

	def checar_lado(self):
		if self.lado == 1:
			self.imagem = pygame.transform.flip(self.imagem, True, False)

	def get_info(self):
		return [str(self.x), str(self.y), str(self.w), str(self.h), str(self.vel_x), str(self.vel_y), str(self.vel), str(self.ativo), str(self.intervalo), str(self.lado), str(self.cor), str(self.caminho_imagem), str(self.__imagem_bala)]

	def clonar(self):
		return Inimigo(self.x, self.y, self.w, self.h, self.vel_x, self.vel_y, self.vel, self.ativo, self.intervalo, self.lado, self.cor, self.caminho_imagem, self.__imagem_bala)

	def __restaurar_intervalo(self):
		self.intervalo = self.__intervalo_original

	def __adicionar_projetil(self):
		if self.lado == 0:
			self.adicionar_projetil(self.x, self.y + self.h / 2 - 5, 5, 5, self.vel, self.lado, self.__imagem_bala)
		else:
			self.adicionar_projetil(self.x + self.w, self.y + self.h / 2 - 5, 5, 5, self.vel, self.lado, self.__imagem_bala)

	def logica(self, jogador):

		if self.ativo:

			if self.intervalo <= 0:
				self.__adicionar_projetil()
				self.__restaurar_intervalo()
			else:
				self.intervalo -= 0.1
			
			self.logica_arma(jogador)

	def desenhar(self, superficie, pos, camera, dt):

		if not self.imagem:
			self.inicializar()
			self.checar_lado()
		
		#superficie.blit(self.imagem, (self.x, self.y))
		superficie.blit(self.imagem, pos)		
		self.desenhar_projeteis(superficie, camera, dt)