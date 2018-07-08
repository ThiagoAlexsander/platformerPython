import pygame

def parse_tuple(string):
	try:
		s = eval(str(string))
		if type(s) == tuple:
			return s
		return
	except:
		return

class Fase(object):

	def __init__(self, _id, jogador, fundo, plataformas, moedas, energias, inimigos, caminho_fundo, cor = (65, 65, 65)):

		self.__fundo = fundo
		self.__caminho_fundo = caminho_fundo
		self.__plataformas = plataformas
		self.__moedas = moedas
		self.__energias = energias
		self.__inimigos = inimigos
		self.__id = _id
		self.__jogador = jogador
		self.cor = cor

	def set_id(self, _id):
		self.__id = _id

	def setar_atributos(self, atributos):

		if atributos[0] != "":
			self.__id = int(atributos[0])

		if atributos[1] != "":
			self.cor = parse_tuple(atributos[1])
			self.__fundo.fill(self.cor)

		if atributos[2] != "":

			if atributos[2] and not "no_img" in atributos[2]:
				self.__caminho_fundo = atributos[2]
				self.__fundo = pygame.image.load("Imagens/"+atributos[2])
			else:
				self.__caminho_fundo = "no_img"
				self.__fundo = pygame.Surface((800, 600))
				self.__fundo.fill(self.cor)

	def remover(self, entidade):
		classe = entidade.__class__.__name__

		if classe == "Plataforma" or classe == "PlataformaAndante":
			self.__plataformas.remove(entidade)
		elif classe == "Moeda":
			self.__moedas.remove(entidade)
		elif classe == "Energia":
			self.__energias.remove(entidade)
		elif classe == "Inimigo":
			self.__inimigos.remove(entidade)
		elif classe == "Jogador":
			self.__jogador = None

	def adicionar(self, entidade):
		classe = entidade.__class__.__name__

		if classe == "Plataforma" or classe == "PlataformaAndante":
			self.__plataformas.append(entidade)
		elif classe == "Moeda":
			self.__moedas.append(entidade)
		elif classe == "Energia":
			self.__energias.append(entidade)
		elif classe == "Inimigo":
			self.__inimigos.append(entidade)
		elif classe == "Jogador":
			self.__jogador = None

	def adicionar_plataforma(self, plataforma):
		self.__plataformas.append(plataforma)

	def adicionar_moeda(self, moeda):
		self.__moedas.append(moeda)

	def adicionar_energia(self, energia):
		self.__energias.append(energia)

	def adicionar_inimigo(self, inimigo):
		self.__inimigos.append(inimigo)

	def set_jogador(self, jogador):
		self.__jogador = jogador

	def get_caminho_fundo(self):
		return self.__caminho_fundo

	def get_cor(self):
		return self.cor

	def get_id(self):
		return self.__id

	def get_fundo(self):
		return self.__fundo

	def get_jogador_ref(self):
		return self.__jogador

	def get_jogador(self):
		if self.__jogador:
			return self.__jogador.clonar()

	def get_plataformas_ref(self):
		return self.__plataformas

	def get_plataformas(self):
		return self.__plataformas[:]

	def get_moedas_ref(self):
		return self.__moedas

	def get_moedas(self):
		return self.__moedas[:]

	def get_energias_ref(self):
		return self.__energias

	def get_energias(self):
		return self.__energias[:]

	def get_inimigos_ref(self):
		return self.__inimigos

	def get_inimigos(self):
		return self.__inimigos[:]

	def clonar(self):

		plats = []
		for plat in self.__plataformas:
			plats.append(plat.clonar())

		moedas = []
		for moe in self.__moedas:
			moedas.append(moe.clonar())

		energias = []
		for ene in self.__energias:
			energias.append(ene.clonar())

		inimigos = []
		for ini in self.__inimigos:
			inimigos.append(ini.clonar())

		return Fase(self.__id, self.__jogador, self.__fundo, plats, moedas, energias, inimigos, self.__caminho_fundo, self.cor)
