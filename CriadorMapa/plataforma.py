import pygame
from entidade import Entidade
from sprite import *

class Plataforma(Entidade, Sprite):

	def __init__(self, x, y, w, h, vel_x = 0, vel_y = 0, vel = 1, cor = (200, 0, 150), imagem = None):

		Entidade.__init__(self, x, y, w, h, vel_x, vel_y, vel)
		Sprite.__init__(self, imagem, cor, 1)

		self.cor = cor

	def get_nomes(self):
		return ["Posicao X","Posicao Y","Largura","Altura","Velocidade X","Velocidade Y","Velocidade","Cor","Imagem"]

	def setar_atributos(self, atributos):
		if atributos[0] != "":
			self.x = float(atributos[0])
		if atributos[1] != "":
			self.y = float(atributos[1])
		if atributos[2] != "":
			self.w = float(atributos[2])
			self.inicializar()
		if atributos[3] != "":
			self.h = float(atributos[3])
			self.inicializar()
		if atributos[4] != "":
			self.vel_x = float(atributos[4])
		if atributos[5] != "":
			self.vel_y = float(atributos[5])
		if atributos[6] != "":
			self.vel = float(atributos[6])
		if atributos[7] != "":
			self.cor = parse_tuple(atributos[7])
			self.imagem.fill(self.cor)
		if atributos[8] != "":
			self.caminho_imagem = atributos[8]
			self.inicializar()

	def get_tipo(self):
		return "plataforma"

	def get_info(self):
		return [str(self.x), str(self.y), str(self.w), str(self.h), str(self.vel_x), str(self.vel_y), str(self.vel), str(self.cor), str(self.caminho_imagem)]

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

	def __init__(self, x, y, w, h, vel_x = 0, vel_y = 0, vel = 1, limite_x = (100, 700), limite_y = (100, 500), intervalo = 10.0, cor = (200, 0, 150), imagem=None):

		Plataforma.__init__(self, x, y, w, h, vel_x, vel_y, vel, cor, imagem)

		self.__movimentando = False
		self.__intervalo = intervalo
		self.__limite_x = limite_x #(x - limite_x[0], x + limite_x[1])
		self.__limite_y = limite_y #(y - limite_y[0], y + limite_y[1])
		self.move_type = ""

		self.__intervalo_original = intervalo

	def get_nomes(self):
		return ["Posicao X", "Posicao Y", "Largura", "Altura", "Velocidade X", "Velocidade Y", "Velocidade", "Limite X", "Limite Y", "Intervalo", "Cor", "Caminho Imagem"]

	def setar_atributos(self, atributos):
		if atributos[0] != "":
			self.x = float(atributos[0])
		if atributos[1] != "":
			self.y = float(atributos[1])
		if atributos[2] != "":
			self.w = float(atributos[2])
			self.inicializar()
		if atributos[3] != "":
			self.h = float(atributos[3])
			self.inicializar()
		if atributos[4] != "":
			self.vel_x = float(atributos[4])
		if atributos[5] != "":
			self.vel_y = float(atributos[5])
		if atributos[6] != "":
			self.vel = float(atributos[6])
		if atributos[7] != "":
			atributos[7] = parse_tuple(atributos[7])
			if atributos[7][0] == 0 and atributos[7][1] == 0:
				self.__limite_x = (0, 0)
			else:
				self.__limite_x = (self.x - atributos[7][0], self.x + self.w + atributos[7][1])
		if atributos[8] != "":
			atributos[8] = parse_tuple(atributos[8])
			if atributos[8][0] == 0 and atributos[8][1] == 0:
				self.__limite_y = (0, 0)
			else:
				self.__limite_y = (self.y - atributos[8][0], self.y + atributos[8][1])
		if atributos[9] != "":
			self.__intervalo = float(atributos[9])
			self.__intervalo_original = float(atributos[9])
		if atributos[10] != "":
			self.cor = parse_tuple(atributos[10])
			self.imagem.fill(self.cor)
		if atributos[11] != "":
			self.caminho_imagem = atributos[11]
			self.inicializar()

	def __str__(self):
		return str(self.move_type)

	def get_tipo(self):
		return "plataforma_andante"

	def get_info(self):
		return [str(self.x), str(self.y), str(self.w), str(self.h), str(self.vel_x), str(self.vel_y), str(self.vel), str(self.__limite_x), str(self.__limite_y), str(self.__intervalo), str(self.cor), str(self.caminho_imagem)]

	def clonar(self):
		return PlataformaAndante(self.x, self.y, self.w, self.h, self.vel_x, self.vel_y, self.vel, self.__limite_x, self.__limite_y, self.__intervalo, self.cor, self.caminho_imagem)

	def restaurar_intervalo(self):
		self.__intervalo = self.__intervalo_original

	def iniciar(self):
		self.iniciar_movimento()

	def logica(self):

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