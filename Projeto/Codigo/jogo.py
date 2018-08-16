from sys import version
from gui import GUI
print(version)

try:
	import pygame
except ImportError:
	from os import system
	system("pip install pygame-1.9.3-cp37-cp37m-win_amd64.whl")
	system("pip install pygame-1.9.3-cp37-cp37m-win32")
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

		self.__FPS = 120
		self.clock = pygame.time.Clock()
		self.__tela = pygame.display.set_mode((800, 600))
		self.__gFase = GerenciadorFase()
		self.__jogador = None
		self.__rodando = False
		self.__pausado = False
		self.__gui = GUI(0, 0, 150, 100, (10, 10, 10), 100)

		self.camera = Camera(800, 600)

		self.__qnt_moedas = 0

	def __inicializar(self):

		self.__rodando = True
		self.__gFase.iniciar()
		self.__jogador = self.__gFase.get_jogador()
		#	self.__jogador.set_vida(3)

		self.__gui.adicionar_texto(15, 0, 0, 15, 15, "Fase atual: " + str(self.__gFase.get_id()), 40)
		self.__gui.adicionar_texto(15, 0, 15, 30, 30, "Moedas: " + str(self.get_total_moedas()), 40)

		for plat in self.__gFase.get_plataformas():
			plat.iniciar()

		#self.__plataforma = Plataforma(400, 200, 100, 30, 0, 0, 0.1, (300, 500), (0, 0))

	def get_total_moedas(self):
		return self.__qnt_moedas

	def adicionar_moeda(self):
		self.__qnt_moedas += 1

	def __logica(self, dt):
		energias = self.__gFase.get_energias()
		inimigos = self.__gFase.get_inimigos()
		moedas = self.__gFase.get_moedas()
		plats = self.__gFase.get_plataformas()
		#print(self.__jogador.get_vida())
		#print(self.__jogador.get_total_moedas())

		if self.__jogador.get_vida() < 1:

			self.__qnt_moedas = 0
			self.__jogador = self.__gFase.resetar()
			#self.__jogador = self.__jogador.clonar()
			#self.__jogador = self.__gFase.get_jogador()

			for ene in energias:
				ene.resetar()

			for moe in moedas:
				moe.resetar()

			return

		#print(self.__jogador.get_vida())

		self.__jogador.logica(dt, plats)
		
		for plat in plats:
			plat.logica()

		for ene in energias:
			ene.logica(self.__jogador)

		for ini in inimigos:
			ini.logica(self.__jogador)

		for moe in moedas:
			if moe.get_ativo():
				colidiu = moe.logica(self.__jogador)
				if colidiu:
					self.adicionar_moeda()

				moe.iniciar_animacao_alpha()
			
		if self.__gFase.objetivo_completo():
			if self.__gFase.passar_fase():
				self.__jogador = self.__gFase.reiniciar_fase_atual()
			else:
				self.mostrar_tela_fim()
		
		if self.__jogador.y > self.__gFase.get_objeto_mais_baixo()[1]:
			self.__jogador = self.__gFase.reiniciar_fase_atual()

	def mostrar_tela_fim(self):

		self.__tela.fill((0, 0, 0))

		menu = True

		while menu:

			self.clock.tick(self.__FPS)

			for e in pygame.event.get():

				if e.type == pygame.QUIT:
					menu = False					
					self.__rodando = False

				if e.type == pygame.KEYDOWN:

					if e.key == pygame.K_r:
						menu = False
						self.__gFase.recomecar()
						self.__jogador = self.__gFase.reiniciar_fase_atual()

					if e.key == pygame.K_ESCAPE:
						menu = False				
						self.__rodando = False

			pygame.display.flip()

	def rodar(self):

		self.__inicializar()
		dt = 0
		while self.__rodando:

			self.__evento()
			self.__atualizar(dt)
			self.__desenhar(dt)

			dt = self.clock.tick(self.__FPS) / 1000.0

	def __evento(self):

		for e in pygame.event.get():

			if e.type == pygame.QUIT:
				self.__rodando = False

			elif e.type == pygame.MOUSEBUTTONDOWN:

				if e.button == 1:

					# HACK

					pos = pygame.mouse.get_pos()
					print(self.__jogador.y)
					print(self.__jogador.vel_y)
					print(pos[1])
					qnt = pos[1] - self.__jogador.y
					#self.__jogador.set_vel_y(-600 + pos[1])
					self.__jogador.set_vel_y(pos[1]-600)

			elif e.type == pygame.KEYDOWN:

				if e.key == pygame.K_ESCAPE:
					self.__rodando = False

				if pygame.key.get_mods() & pygame.KMOD_SHIFT and e.key == pygame.K_RETURN:
					if self.__gFase.passar_fase():
						self.__jogador = self.__gFase.reiniciar_fase_atual()

				elif e.key == pygame.K_RETURN:
					# HACK
					self.__jogador.set_y(-1200)

	def __desenhar(self, dt):

		self.__tela.blit(self.__gFase.get_fundo(), (0,0))

		self.__jogador.desenhar(self.__tela, self.camera.aplicar(self.__jogador, dt))


		for plat in self.__gFase.get_plataformas():
			plat.desenhar(self.__tela, self.camera.aplicar(plat, dt))

		for ene in self.__gFase.get_energias():
			ene.desenhar(self.__tela, self.camera.aplicar(ene, dt))

		for ini in self.__gFase.get_inimigos():
			ini.desenhar(self.__tela, self.camera.aplicar(ini, dt), self.camera, dt)

		for moe in self.__gFase.get_moedas():
			moe.desenhar(self.__tela, self.camera.aplicar(moe, dt))

		self.__gui.desenhar(self.__tela)

	def __atualizar(self, dt):

		self.__logica(dt)
		self.camera.atualizar(self.__jogador)

		self.__gui.definir_texto(0, "Fase atual: " + str(self.__gFase.get_id()))
		self.__gui.definir_texto(1, "Moedas: " + str(self.get_total_moedas()))

		#print(self.__gFase.get_objeto_mais_baixo())

		pygame.display.flip()

if __name__ == "__main__":

	jogo = Jogo()
	jogo.rodar()