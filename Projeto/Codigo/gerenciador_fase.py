try:
	import glob
except ImportError:
	from os import system
	system("pip install glob")

from fase import Fase
from fabrica_fases import FabricaFases

class GerenciadorFase(object):

	def __init__(self):

		self.__fs = FabricaFases()
		self.__fase_atual = None
		self.__lista_fases = []
		self.__lista_fases_original = []

	def iniciar(self):
		self.__carregar_fases()

	def reiniciar_fase_atual(self):

		for plat in self.get_plataformas():
			plat.iniciar()

		return self.get_jogador()

	def get_fase_com_id(self, _id):
		for i in range(len(self.__lista_fases_original)):
			if self.__lista_fases[i].get_id() == _id:
				return self.__lista_fases_original[i].clonar()

		return None

	def resetar(self):
		fase_atual_id_antigo = self.__fase_atual.get_id()
		#for plat in self.__fase_atual.get_plataformas():
			#if plat.__class__.__name__ == "PlataformaAndante":
				#print("OLD PlataformaAndante:",plat.x, plat.y)
		#print("OLD",self.__lista_fases)
		self.__restaurar_lista_fases()
		#print("NEW",self.__lista_fases)
		fase = self.get_fase_com_id(fase_atual_id_antigo)
		if fase:
			self.__set_fase_atual(fase)
			#for plat in self.__fase_atual.get_plataformas():
			#	if plat.__class__.__name__ == "PlataformaAndante":
			#		print("NEW PlataformaAndante:",plat.x, plat.y)

		return self.reiniciar_fase_atual()

	def __adicionar_fase(self, fase):
		self.__lista_fases_original.append(fase.clonar())

	def __restaurar_lista_fases(self):
		l = []
		for f in self.__lista_fases_original:
			l.append(f.clonar())
		self.__lista_fases = l

	def __carregar_fases(self):
		#os.chdir("./Fases")
		arquivos = glob.glob("../Fases/*.gload")
		#arquivos = [f for f in os.listdir('.') if os.path.isfile(f)]
		print(arquivos)
		for arquivo in arquivos:
			if ".gload" in arquivo:
				#print(arquivo)
				fase = self.__fs.criar_fase(self.__fs.carregar_arquivo(arquivo))
				
				#self.__lista_fases_original.append(fase)
				self.__adicionar_fase(fase)

		self.__restaurar_lista_fases()
		self.__set_fase_atual(self.get_fase_com_id(0))

	def __set_fase_atual(self, fase):
		self.__fase_atual = fase

	def passar_fase(self):
		for fase in self.__lista_fases:
			if self.__fase_atual.get_id() + 1 == fase.get_id():
				self.__set_fase_atual(fase)
				return True

		return False

	def get_id(self):
		return self.__fase_atual.get_id()

	def get_fundo(self):
		return self.__fase_atual.get_fundo()

	def get_fases(self):
		return self.__lista_fases

	def get_plataformas(self):
		return self.__fase_atual.get_plataformas()

	def get_jogador_ref(self):
		return self.__fase_atual.get_jogador_ref()

	def get_jogador(self):
		return self.__fase_atual.get_jogador()

	def get_energias(self):
		return self.__fase_atual.get_energias()

	def get_inimigos(self):
		return self.__fase_atual.get_inimigos()

	def get_moedas(self):
		return self.__fase_atual.get_moedas()

	def objetivo_completo(self):
		ativos = []
		for i in self.__fase_atual.get_energias():
			ativos.append(i.get_ativo())

		#print(ativos)
		if True in ativos:
			return False
		else:
			return True
