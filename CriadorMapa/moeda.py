from entidade import Entidade
from sprite import *

class Moeda(Entidade, Sprite):

	def __init__(self, x, y, w, h, vel_x = 0, vel_y = 0, vel = 1, cor = (200, 0, 150), imagem=None):

		Entidade.__init__(self, x, y, w, h, vel_x, vel_y, vel)
		Sprite.__init__(self, imagem, cor, 1, 100, 204, 0.7)
		self.__ativo = True
		#self.angulo = 0

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