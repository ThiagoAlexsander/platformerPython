from sys import version
from gui import GUI
print(version)

try:
	import pygame
except ImportError:
	from os import system
	system("pip install pygame-1.9.3-cp37-cp37m-win_amd64.whl")
	system("pip install pygame-1.9.3-cp37-cp37m-win32")
	system("pip install pygame")
	system("pip install pygame --user")
	#from sys import exit
	#exit()
	import pygame

from gerenciador_fase import GerenciadorFase
from jogador import Jogador
from plataforma import Plataforma

from camera import Camera

pygame.init()

class Jogo(object):

	def __init__(self):

		self.FPS = 120
		self.clock = pygame.time.Clock()
		self.tela = pygame.display.set_mode((800, 600))
		self.gFase = GerenciadorFase()
		self.jogador = None
		self.__rodando = False
		self.__pausado = False
		self.__gui = GUI(0, 0, 150, 100, (10, 10, 10), 100)
		self.__gui2 = GUI(0, 0, 800, 600, (0, 0, 0), 255)

		self.camera = Camera(800, 600)

		self.__qnt_moedas = 0

	def __inicializar(self):

		self.__rodando = True
		self.gFase.iniciar()
		self.jogador = self.gFase.get_jogador()
		#	self.jogador.set_vida(3)

		self.__gui.adicionar_texto(15, 0, 0, 15, 15, "Fase atual: " + str(self.gFase.get_id()), 40)
		self.__gui.adicionar_texto(15, 0, 15, 30, 30, "Moedas: " + str(self.get_total_moedas()), 40)

		for plat in self.gFase.get_plataformas():
			plat.iniciar()

		#self.__plataforma = Plataforma(400, 200, 100, 30, 0, 0, 0.1, (300, 500), (0, 0))

	def get_total_moedas(self):
		return self.__qnt_moedas

	def adicionar_moeda(self):
		self.__qnt_moedas += 1

	def __logica(self, dt):
		energias = self.gFase.get_energias()
		inimigos = self.gFase.get_inimigos()
		moedas = self.gFase.get_moedas()
		plats = self.gFase.get_plataformas()

		#print(self.jogador.get_vida())
		#print(self.jogador.get_total_moedas())

		if self.jogador.get_vida() < 1:

			self.__qnt_moedas = 0
			self.jogador = self.gFase.resetar()
			#self.jogador = self.jogador.clonar()
			#self.jogador = self.gFase.get_jogador()

			for ene in energias:
				ene.resetar()

			for moe in moedas:
				moe.resetar()

			return

		#print(self.jogador.get_vida())

		self.jogador.logica(dt, plats)
		
		for plat in plats:
			plat.logica()

		for ene in energias:
			ene.logica(self.jogador)

		for ini in inimigos:
			ini.logica(self.jogador)

		for moe in moedas:
			if moe.get_ativo():
				colidiu = moe.logica(self.jogador)
				if colidiu:
					self.adicionar_moeda()

				moe.iniciar_animacao_alpha()
			
		if self.gFase.objetivo_completo():
			if self.gFase.passar_fase():
				self.jogador = self.gFase.reiniciar_fase_atual()
			else:
				self.mostrar_tela_fim()
		
		if self.jogador.y > self.gFase.get_objeto_mais_baixo()[1]:
			self.jogador = self.gFase.reiniciar_fase_atual()	

	def rodar(self):

		self.__inicializar()
		dt = 0
		while self.__rodando:

			self.__evento()
			self.__atualizar(dt)
			self.__desenhar(dt)

			dt = self.clock.tick(self.FPS) / 1000.0

	def __evento(self):

		for e in pygame.event.get():

			if e.type == pygame.QUIT:
				self.__rodando = False

			elif e.type == pygame.MOUSEBUTTONDOWN:

				if e.button == 1:

					# HACK

					pos = pygame.mouse.get_pos()
					print(self.jogador.y)
					print(self.jogador.vel_y)
					print(pos[1])
					qnt = pos[1] - self.jogador.y
					#self.jogador.set_vel_y(-600 + pos[1])
					self.jogador.set_vel_y(pos[1]-600)

			elif e.type == pygame.KEYDOWN:

				if e.key == pygame.K_ESCAPE:
					self.__rodando = False

				if pygame.key.get_mods() & pygame.KMOD_SHIFT and e.key == pygame.K_RETURN:
					if self.gFase.passar_fase():
						self.jogador = self.gFase.reiniciar_fase_atual()

				elif e.key == pygame.K_RETURN:
					# HACK
					self.jogador.set_y(-1200)

	def mostrar_tela_fim(self):

		menu = True
		textos = ["Fim do jogo!", "Pressione R para recomecar o jogo.", "Aperte ESC para sair do jogo."]

		self.__gui2.adicionar_texto(40, 410 - (40 * len(textos[0])), 200-40, 40, 50, textos[0], 100, (255, 100, 105))
		self.__gui2.adicionar_texto(40, 410 - (40 * len(textos[1])), 300-40, 40, 50, textos[1], 100, (255, 100, 105))
		self.__gui2.adicionar_texto(40, 410 - (40 * len(textos[2])), 400-40, 40, 50, textos[2], 100, (255, 100, 105))

		while menu:
			self.tela.fill((255, 105, 20))
			for e in pygame.event.get():

				if e.type == pygame.QUIT:
					menu = False
					self.__rodando = False

				if e.type == pygame.KEYDOWN:

					if e.key == pygame.K_r:
						menu = False
						self.gFase.recomecar()
						self.jogador = self.gFase.reiniciar_fase_atual()
						self.__qnt_moedas = 0 

					if e.key == pygame.K_ESCAPE:
						menu = False
						self.__rodando = False

			self.__gui2.desenhar(self.tela)

			self.clock.tick(self.FPS)
			pygame.display.flip()

	def __desenhar(self, dt):

		self.tela.blit(self.gFase.get_fundo(), (0,0))

		self.jogador.desenhar(self.tela, self.camera.aplicar(self.jogador, dt))


		for plat in self.gFase.get_plataformas():
			plat.desenhar(self.tela, self.camera.aplicar(plat, dt))

		for ene in self.gFase.get_energias():
			ene.desenhar(self.tela, self.camera.aplicar(ene, dt))

		for ini in self.gFase.get_inimigos():
			ini.desenhar(self.tela, self.camera.aplicar(ini, dt), self.camera, dt)

		for moe in self.gFase.get_moedas():
			moe.desenhar(self.tela, self.camera.aplicar(moe, dt))

		self.__gui.desenhar(self.tela)

	def __atualizar(self, dt):

		self.__logica(dt)
		self.camera.atualizar(self.jogador)

		self.__gui.definir_texto(0, "Fase atual: " + str(self.gFase.get_id()))
		self.__gui.definir_texto(1, "Moedas: " + str(self.get_total_moedas()))

		#print(self.gFase.get_objeto_mais_baixo())

		pygame.display.flip()

if __name__ == "__main__":

	jogo = Jogo()
	jogo.rodar()