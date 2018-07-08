from projetil import Projetil

class Arma(object):

	def __init__(self, ativo, intervalo, lado):

		self.__lista_projeteis = []
		self.ativo = ativo
		self.intervalo = intervalo
		self.lado = lado

	def logica_arma(self, jogador):

		for proj in self.__lista_projeteis[:]:
			if proj.ativo:
				proj.logica(jogador)
			else:
				self.__remover_projetil(proj)

	def adicionar_projetil(self, x, y, w, h, vel, lado, imagem, cor = (255, 255, 255), vel_x = 0.0, vel_y = 0.0):
		self.__lista_projeteis.append(Projetil(x, y, w, h, vel_x, vel_y, vel, lado, cor, imagem))

	def __remover_projetil(self, projetil):
		self.__lista_projeteis.remove(projetil)

	def desenhar_projeteis(self, superficie, camera, dt):
		
		for proj in self.__lista_projeteis:
			if proj.ativo:
				proj.desenhar(superficie, camera.aplicar(proj, dt))

	def get_projeteis(self):
		return self.__lista_projeteis