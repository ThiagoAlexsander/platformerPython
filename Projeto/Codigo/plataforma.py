import pygame
from entidade import Entidade
from sprite import Sprite

class Plataforma(Entidade, Sprite):

	def __init__(self, x, y, w, h, vel_x = 0, vel_y = 0, vel = 1, cor = (200, 0, 150), imagem = None):

		Entidade.__init__(self, x, y, w, h, vel_x, vel_y, vel)
		Sprite.__init__(self, imagem, cor)

		self.cor = cor

	def clonar(self):
		return Plataforma(self.x, self.y, self.w, self.h, self.vel_x, self.vel_y, self.vel, self.cor, self.caminho_imagem)

	def iniciar(self):
		pass

	def logica(self):
		pass
			
	def desenhar(self, superficie, pos):

		if not self.imagem:
			self.inicializar()

		#superficie.blit(self.imagem, (self.x, self.y))
		superficie.blit(self.imagem, pos)
		
	def get_cor(self):
		return self.cor

class PlataformaAndante(Plataforma):

	def __init__(self, x, y, w, h, vel_x = 0, vel_y = 0, vel = 1, limite_x = (100, 100), limite_y = (0, 0), intervalo = 10.0, cor = (200, 0, 150), imagem=None):

		Plataforma.__init__(self, x, y, w, h, vel_x, vel_y, vel, cor, imagem)

		self.__movimentando = False
		#self.__limite_x = limite_x
		#self.__limite_y = limite_y
		self.__intervalo = intervalo
		self.__limite_x = limite_x #_lazy = (x - limite_x[0], x + limite_x[1])
		self.__limite_y = limite_y #_lazy = (y - limite_y[0], y + limite_y[1])
		self.move_type = ""
		self.primeira_vez = True

		self.__intervalo_original = intervalo

	def get_posicao_inicial(self):
		return (self.__limite_x[0], self.__limite_y[1])

	def __str__(self):
		return str(self.move_type)

	def clonar(self):
		return PlataformaAndante(self.x, self.y, self.w, self.h, self.vel_x, self.vel_y, self.vel, self.__limite_x, self.__limite_y, self.__intervalo, self.cor, self.caminho_imagem)

	def restaurar_intervalo(self):
		self.__intervalo = self.__intervalo_original

	def iniciar(self):
		self.iniciar_movimento()

	def logica(self):
		if self.__intervalo > 0:
			self.__intervalo -= 0.1
		elif self.__intervalo <= 0:
			self.restaurar_intervalo()
			self.primeira_vez = False

		if not self.primeira_vez:
			if self.__movimentando:
				if self.__limite_y[0] == 0 and self.__limite_y[1] == 0:
					self.move_type = "horizontal"
					if self.x + self.w > self.__limite_x[1]:
						self.__intervalo -= 0.1
						if self.__intervalo <= 0:
							self.vel_x = -self.vel
							self.restaurar_intervalo()
						else:
							self.vel_x = 0

					elif self.x < self.__limite_x[1] and self.x < self.__limite_x[0]:

						self.__intervalo -= 0.1
						if self.__intervalo <= 0:
							self.vel_x = self.vel
							self.restaurar_intervalo()
						else:
							self.vel_x = 0

					self.x += self.vel_x
				else:
					self.move_type = "vertical"
					if self.y + self.h > self.__limite_y[1]:
						self.__intervalo -= 0.1
						if self.__intervalo <= 0:
							self.vel_y = -self.vel
							self.restaurar_intervalo()
						else:
							self.vel_y = 0

					elif self.y < self.__limite_y[1] and self.y < self.__limite_y[0]:
						self.__intervalo -= 0.1
						if self.__intervalo <= 0:
							self.vel_y = self.vel
							self.restaurar_intervalo()
						else:
							self.vel_y = 0

					self.y += self.vel_y

	def iniciar_movimento(self):
		if self.__limite_x[0] != 0 and self.__limite_x[1] != 0:
			self.vel_x = self.vel
			self.__movimentando = True
		if self.__limite_y[0] != 0 and self.__limite_y[1] != 0:
			self.vel_y = self.vel
			self.__movimentando = True

	def parar_movimento(self):
		self.__movimentando = False
		#self.set_vel_x(0.0)
		#self.set_vel_y(0.0)
		#self.set_vel(0.0)

	def get_movimentando(self):
		return self.__movimentando