class Fase(object):

	def __init__(self, _id, jogador, fundo, plataformas, moedas, energias, inimigos, cor = (65, 65, 65)):

		self.__fundo = fundo
		self.__plataformas = plataformas
		self.__moedas = moedas
		self.__energias = energias
		self.__inimigos = inimigos
		self.__id = _id
		self.__jogador = jogador
		self.cor = cor
		
	def get_id(self):
		return self.__id

	def get_cor(self):
		return self.cor

	def get_jogador_ref(self):
		return self.__jogador

	def get_jogador(self):
		return self.__jogador.clonar()

	def get_fundo(self):
		return self.__fundo

	def get_plataformas(self):
		return self.__plataformas[:]

	def get_moedas(self):
		return self.__moedas[:]

	def get_energias(self):
		return self.__energias[:]

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

		return Fase(self.__id, self.__jogador, self.__fundo, plats, moedas, energias, inimigos, self.cor)
