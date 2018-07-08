from arma import Arma
from entidade import Entidade
from sprite import *
import pygame

class Inimigo(Entidade, Sprite, Arma):

	def __init__(self, x, y, w, h, vel_x, vel_y, vel, ativo = True, intervalo = 3.0, lado = 0, cor = (0, 25, 125), imagem = None, imagem_bala = None):

		Entidade.__init__(self, x, y, w, h, vel_x, vel_y, vel)
		Sprite.__init__(self, imagem, cor, 2)
		Arma.__init__(self, ativo, intervalo, lado)

		self.__cor = cor
		self.__intervalo_original = intervalo
		self.__imagem_bala = imagem_bala

	def get_nomes(self):
		return ["Posicao X","Posicao Y","Largura","Altura","Velocidade X","Velocidade Y", "Intervalo", "Lado", "Velocidade", "Cor", "Caminho Imagem", "Caminho Imagem Projetil"]

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
			self.intervalo = float(atributos[6])
			self.__intervalo_original = float(atributos[6])

		if atributos[7] != "":
			self.lado = parse_bool(atributos[7])
			self.inicializar()
			self.checar_lado()

		if atributos[8] != "":
			self.vel = float(atributos[8])

		if atributos[9] != "":
			self.cor = parse_tuple(atributos[9])
			self.imagem.fill(self.cor)

		if atributos[10] != "":
			self.caminho_imagem = atributos[10]
			self.inicializar()

		if atributos[11] != "":
			self.__imagem_bala = atributos[11]
			self.inicializar()


	def checar_lado(self):
		if self.lado == 1:
			print(self.__imagem_bala)
			print(self.lado)
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