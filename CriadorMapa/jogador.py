import pygame
from entidade import Entidade
from sprite import *

class Jogador(Entidade, Sprite):

	def __init__(self, x, y, w, h, vel_x, vel_y, vel, cor = (0, 25, 125), imagem=None):

		Entidade.__init__(self, x, y, w, h, vel_x, vel_y, vel)
		Sprite.__init__(self, imagem, cor, 2)

		self.__qnt_moedas = 0
		self.__vida = 3
		self.__gravidade = 5.8 #3.2
		self.__cor = cor
		self.__no_chao = False

	def get_nomes(self):
		return ["Posicao X","Posicao Y","Largura","Altura","Velocidade X","Velocidade Y","Velocidade","Cor","Caminho Imagem"]

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

	def get_info(self):
		return [str(self.x), str(self.y), str(self.w), str(self.h), str(self.vel_x), str(self.vel_y), str(self.vel), str(self.cor), str(self.caminho_imagem)]

	def clonar(self):
		return Jogador(self.x, self.y, self.w, self.h, self.vel_x, self.vel_y, self.vel, self.cor, self.caminho_imagem)

	def resetar(self):
		self.__qnt_moedas = 0
		self.__vida = 3

	def desenhar(self, superficie, pos):

		if not self.imagem:
			self.inicializar()

		#superficie.blit(self.imagem, (self.x, self.y))
		
		superficie.blit(self.imagem, pos)
			
	def __pular(self, ents):
		
		if self.__no_chao:

			self.vel_y = -360 #-240 #-350
			self.__no_chao = False

	def __evento(self, ents):
		e = pygame.key.get_pressed() # Pega os eventos.

		if e[pygame.K_LEFT]:
			self.vel_x += -self.vel

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
						self.vel_y = -self.__gravidade - ent.vel_y
						self.vel_x += ent.vel_x

			elif self.vel_y > -self.__gravidade and dt != 1:
				self.__no_chao = False
				
			if self.colidindo_baixo(ent):

				if self.y < ent.y + ent.h + 3.6:

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

	def adicionar_moeda(self):
		self.__qnt_moedas += 1

	def adicionar_vida(self):
		self.__vida += 1

	def subtrair_vida(self):
		self.__vida -= 1

	def get_vida(self):
		return self.__vida

	def set_vida(self, vida):
		self.__vida = vida

	def get_total_moedas(self):
		return self.__qnt_moedas

	def get_cor(self):
		return self.__cor
