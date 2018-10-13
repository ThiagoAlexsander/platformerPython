import pygame

class GUI(object):

	def __init__(self, tela):
		self.tela = tela
		self.fontes = (pygame.font.SysFont('Comic Sans MS', 20), pygame.font.SysFont('Comic Sans MS', 50))

	def desenhar_volume(self, volume):
		self.tela.blit(self.fontes[0].render("Volume: " + str(int((volume)*10)), True, (255,0,0)), (720,0))

	def desenhar_moedas(self, moedas):
		self.tela.blit(self.fontes[0].render("Moedas: " + str(moedas), True, (255,255,0)), (0,0))

	def desenhar_energias(self, energias):
		self.tela.blit(self.fontes[0].render("Energias: " + str(energias), True, (255,255,0)), (0,30))

	def desenhar_fase_atual(self, fase):
		self.tela.blit(self.fontes[1].render("Fase : " + str(fase), True, (75,0,130)), (340,0))