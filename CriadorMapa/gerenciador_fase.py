import glob
import pygame

from fase import Fase
from gerenciador_entidade import GerenciadorEntidade
from fabrica_fases import FabricaFases

class GerenciadorFase(object):

	DUMMY_FUNDO = pygame.Surface((800, 600))
	DUMMY_FUNDO.fill((65, 65, 65))

	def __init__(self):

		self.__fase_atual = Fase(-1, None, self.DUMMY_FUNDO, [], [], [], [], "no_img")
		self.__fs = FabricaFases()
		self.__ge = GerenciadorEntidade(self, self.__fs, self.__fase_atual)
		self.__lista_fases = []
		self.__lista_fases_original = []

	def iniciar(self, nome):
		self.__carregar_fases(nome)
		self.__ge.iniciar(self.__fase_atual)

		entidades = []
		
		if self.__fase_atual:

			for plat in self.get_plataformas():
				entidades.append(plat)
			
			for ini in self.get_inimigos():
				entidades.append(ini)
			
			for ene in self.get_energias():
				entidades.append(ene)
			
			for moe in self.get_moedas():
				entidades.append(moe)
			
			p = self.get_jogador_ref()
			if p:
				entidades.append(p)

			return entidades, self.__fase_atual

		return None

	def __adicionar_fase(self, fase):
		self.__lista_fases_original.append(fase.clonar())

	def __carregar_fases(self, nome):
		arquivos = glob.glob("./Fases/*.gload")
		
		print(arquivos)
		for arquivo in arquivos:
			if "Fases" in arquivo and nome in arquivo:
				fase = self.__fs.criar_fase(self.__fs.carregar_arquivo(arquivo))
				self.__adicionar_fase(fase)
				self.__set_fase_atual(fase)
				break

	def desenhar_fundo(self, tela):
		if not self.__fase_atual: return

		tela.blit(self.__fase_atual.get_fundo(), (0,0))

	def __set_fase_atual(self, fase):
		self.__fase_atual = fase

	def get_gerenciador_entidades(self):
		return self.__ge

	def get_fabrica_fases(self):
		return self.__fs

	def get_fase_atual(self):
		return self.__fase_atual

	def get_id(self):
		return self.__fase_atual.get_id()

	def get_fundo(self):
		return self.__fase_atual.get_fundo()

	def get_fases(self):
		return self.__lista_fases

	def get_jogador_ref(self):
		return self.__fase_atual.get_jogador_ref()

	def get_jogador(self):
		return self.__fase_atual.get_jogador()

	def get_plataformas_ref(self):
		return self.__fase_atual.get_plataformas_ref()

	def get_plataformas(self):
		return self.__fase_atual.get_plataformas()

	def get_energias_ref(self):
		return self.__fase_atual.get_energias_ref()

	def get_energias(self):
		return self.__fase_atual.get_energias()

	def get_inimigos_ref(self):
		return self.__fase_atual.get_inimigos_ref()

	def get_inimigos(self):
		return self.__fase_atual.get_inimigos()

	def get_moedas_ref(self):
		return self.__fase_atual.get_moedas_ref()

	def get_moedas(self):
		return self.__fase_atual.get_moedas()
