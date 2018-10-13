from os import kill, getpid
from menu import Menu
from gui import GUI
from gerenciador_musica import GerenciadorMusica

try:
	import pygame
except ImportError:
	from os import system
	system("pip3 install pygame-1.9.3-cp37-cp37m-win_amd64.whl")
	system("pip3 install pygame-1.9.3-cp37-cp37m-win32")
	system("pip3 install pygame")
	system("pip3 install pygame --user")
	#from sys import exit
	#exit()
	import pygame

from gerenciador_fase import GerenciadorFase
from jogador import Jogador
from plataforma import Plataforma

from camera import Camera

class Jogo(object):

	def __init__(self):

		pygame.init()
		self.FPS = 120
		self.clock = pygame.time.Clock()
		self.tela = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
		self.gFase = GerenciadorFase()
		self.jogador = None
		self.__rodando = False
		self.__pausado = False
		self.tocando = False
		self.__qnt_moedas_fase_atual = 0
		self.__qnt_moedas = 0

		self.camera = Camera(800, 600)
		self.musica = GerenciadorMusica()

		self.menu = Menu(self)
		self.GUI = GUI(self.tela)

	def atualizar_entidades_fase(self):
		self.energias = self.gFase.get_energias()
		self.inimigos = self.gFase.get_inimigos()
		self.moedas = self.gFase.get_moedas()
		self.plats = self.gFase.get_plataformas()

	def __inicializar(self):

		self.__rodando = True
		self.gFase.iniciar()

		self.jogador = self.gFase.get_jogador()

		self.atualizar_entidades_fase()

		self.musica.tocar(self.gFase.get_id())

	def get_energias_restantes(self):
		return self.gFase.get_total_energias()

	def get_total_moedas_fase_atual(self):

		return self.__qnt_moedas_fase_atual

	def get_total_moedas(self):

		return self.__qnt_moedas

	def adicionar_moeda(self):

		self.__qnt_moedas_fase_atual += 1

	def atualizar_fase(self):
		
		self.atualizar_entidades_fase()
		self.jogador = self.gFase.reiniciar_fase_atual()

	def resetar(self):

		self.__qnt_moedas_fase_atual = 0

		self.jogador = self.gFase.resetar()

		self.atualizar_entidades_fase()

		for ene in self.energias:
			ene.resetar()

		for moe in self.moedas:
			moe.resetar()
			
	def __logica(self, dt):
		
		if self.jogador.get_vida() < 1:
			self.resetar()
			return

		self.jogador.logica(dt, self.plats)
		
		for plat in self.plats:
			plat.logica()

		for ene in self.energias:
			ene.logica(self.jogador)

		for ini in self.inimigos:
			ini.logica(self.jogador)

		for moe in self.moedas:
			if moe.get_ativo():
				colidiu = moe.logica(self.jogador)
				if colidiu:
					self.adicionar_moeda()

				moe.iniciar_animacao_alpha()
			
		if self.gFase.objetivo_completo():

			if self.gFase.passar_fase():
				self.atualizar_fase()

				self.menu.definir_menu(1)

				if self.menu.get_opcao() == 1:
					self.__rodando = False

				self.menu.restaurar()

				self.musica.tocar(self.gFase.get_id())

				self.__qnt_moedas += self.__qnt_moedas_fase_atual
				self.__qnt_moedas_fase_atual = 0

			else: # Fim de Jogo ( não há mais fases para se passar )

				self.menu.definir_menu(3)
				opcao = self.menu.get_opcao()

				if opcao == 1:
					self.__rodando = False
				elif opcao == 2:
					self.gFase.recomecar()
					self.resetar()
					self.musica.tocar(self.gFase.get_id())
					self.__qnt_moedas = 0
					self.__qnt_moedas_fase_atual = 0

				self.menu.restaurar()

		if self.jogador.y > self.gFase.get_objeto_mais_baixo()[1] + 200:
			self.jogador.set_vida(0)

	def rodar(self):

		self.menu.definir_menu(0)

		if self.menu.get_opcao() == 0:

			self.__inicializar()
			dt = 0
			while self.__rodando:
				
				dt = self.clock.tick(self.FPS) / 1000.0
				self.__evento()
				self.__atualizar(dt)
				self.__desenhar(dt)
				

	def __evento(self):

		mods = pygame.key.get_mods()

		for e in pygame.event.get():

			if e.type == pygame.QUIT:
				self.__rodando = False

			elif e.type == pygame.MOUSEBUTTONDOWN:

				if e.button == 1:

					# HACK

					pos = pygame.mouse.get_pos()				
					self.jogador.set_vel_y(pos[1]-600)

			elif e.type == pygame.KEYDOWN:

				if e.key == pygame.K_KP_MINUS:
					self.musica.abaixar_volume()

				elif e.key == pygame.K_KP_PLUS:
					self.musica.aumentar_volume()

				if e.key == pygame.K_ESCAPE:

					self.menu.definir_menu(2)
					opcao = self.menu.get_opcao()
					if opcao == 1:
						self.__rodando = False
					elif opcao == 2:
						self.resetar()

					self.menu.restaurar()

				if mods & pygame.KMOD_CTRL | pygame.KMOD_SHIFT and e.key == pygame.K_RETURN:
					
					if self.gFase.passar_fase():
						self.atualizar_fase()
						self.musica.tocar(self.gFase.get_id())

						self.__qnt_moedas += self.__qnt_moedas_fase_atual
						self.__qnt_moedas_fase_atual = 0

				elif mods & pygame.KMOD_SHIFT and e.key == pygame.K_RETURN:

					if self.gFase.passar_fase():

						self.atualizar_fase()

						self.menu.definir_menu(1)
						
						if self.menu.get_opcao() == 1:
							self.__rodando = False

						self.menu.restaurar()

						self.musica.tocar(self.gFase.get_id())

						self.__qnt_moedas += self.__qnt_moedas_fase_atual
						self.__qnt_moedas_fase_atual = 0

				elif e.key == pygame.K_RETURN:

					# HACK

					self.jogador.set_y(-1200)
				

	def __desenhar(self, dt):

		self.tela.blit(self.gFase.get_fundo(), (0,0))

		self.jogador.desenhar(self.tela, self.camera.aplicar(self.jogador, dt))

		for plat in self.plats:
			plat.desenhar(self.tela, self.camera.aplicar(plat, dt))

		for ene in self.energias:
			ene.desenhar(self.tela, self.camera.aplicar(ene, dt))

		for ini in self.inimigos:
			ini.desenhar(self.tela, self.camera.aplicar(ini, dt), self.camera, dt)

		for moe in self.moedas:
			moe.desenhar(self.tela, self.camera.aplicar(moe, dt))

		#TODO: Fazer uma função só para desenhar o HUD.

		self.GUI.desenhar_volume(self.musica.get_volume())
		self.GUI.desenhar_moedas(self.get_total_moedas() + self.get_total_moedas_fase_atual())
		self.GUI.desenhar_energias(self.get_energias_restantes())
		self.GUI.desenhar_fase_atual(self.gFase.get_id())

	def __atualizar(self, dt):

		self.__logica(dt)
		self.camera.atualizar(self.jogador)

		pygame.display.flip()

if __name__ == "__main__":

	jogo = Jogo()
	jogo.rodar()
	try:
		kill(getpid(), 9)
	except:
		print("Não foi possível terminar o processo do python.")