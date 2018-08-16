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
		self.__todos_objetos = []

		for plat in self.__plataformas:
			self.__todos_objetos.append(plat)

		for moe in self.__moedas:
			self.__todos_objetos.append(moe)

		for ene in self.__energias:			
			self.__todos_objetos.append(ene)

		for ini in self.__inimigos:
			self.__todos_objetos.append(ini)

	def get_objeto_mais_baixo(self):
		
		mais_baixo = None
		for i in range(len(self.__todos_objetos)):
			if i == 0:
				mais_baixo = self.__todos_objetos[i]
			elif self.__todos_objetos[i].y > mais_baixo.y:
					mais_baixo = self.__todos_objetos[i]		

		return mais_baixo.get_posicao_inicial()
	
	def get_objetos(self):
		return self.__todos_objetos[:]

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
