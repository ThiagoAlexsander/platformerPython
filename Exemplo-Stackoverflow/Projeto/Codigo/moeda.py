from entidade import Entidade
from sprite import Sprite, pygame

class Moeda(Entidade, Sprite):

	def __init__(self, x, y, w, h, vel_x = 0, vel_y = 0, vel = 1, cor = (200, 0, 150), imagem=None):

		Entidade.__init__(self, x, y, w, h, vel_x, vel_y, vel)
		Sprite.__init__(self, imagem, cor, 100, 204, 0.7)
		self.__ativo = True
		#self.angulo = 0

	def clonar(self):

		return Moeda(self.x, self.y, self.w, self.h, self.vel_x, self.vel_y, self.vel, self.cor, self.caminho_imagem)

	def resetar(self):
		self.__ativo = True

	def logica(self, jogador):

		if self.colidindo(jogador):
			jogador.adicionar_moeda()
			self.__ativo = False

	def desenhar(self, superficie, pos):
		
		if self.__ativo:
			if not self.imagem:
				self.inicializar()
				
			#superficie.blit(self.imagem, (self.x, self.y))
			superficie.blit(self.imagem, pos)

	def get_ativo(self):
		return self.__ativo

	def iniciar_anim(self):
		pass		

	def parar_anim(self):
		pass