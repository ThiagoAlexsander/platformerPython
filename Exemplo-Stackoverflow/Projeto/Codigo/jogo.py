from sys import version
print(version)

try:
	import pygame
except ImportError:
	from os import system
	system("pip install pygame-1.9.3-cp37-cp37m-win_amd64.whl")
	system("pip install pygame-1.9.3-cp37-cp37m-win32")
	from sys import exit
	exit()

from gerenciador_fase import GerenciadorFase
from jogador import Jogador
from plataforma import Plataforma

from camera import Camera

pygame.init()

class Jogo(object):

	def __init__(self):

		self.fps = 120
		self.clock = pygame.time.Clock()
		self.__screen = pygame.display.set_mode((800, 600))
		self.__gFase = GerenciadorFase()
		self.__jogador = None
		self.__rodando = False
		self.__pausado = False
		self.mudar_fps = False

		self.camera = Camera(800, 600)

	def __inicializar(self):

		self.__rodando = True
		self.__gFase.iniciar()
		self.__jogador = self.__gFase.get_jogador()

		for plat in self.__gFase.get_plataformas():
			plat.iniciar()

	def __logica(self, dt):
		energias = self.__gFase.get_energias()
		inimigos = self.__gFase.get_inimigos()
		moedas = self.__gFase.get_moedas()
		plats = self.__gFase.get_plataformas()

		if self.__jogador.get_vida() < 1:
			self.__jogador = self.__gFase.resetar()

			for ene in energias:
				ene.resetar()

			for moe in moedas:
				moe.resetar()

			return

		self.__jogador.logica(dt, plats)
		
		for plat in plats:
			plat.logica()

		for ene in energias:
			ene.logica(self.__jogador)

		for ini in inimigos:
			ini.logica(self.__jogador)

		for moe in moedas:
			if moe.get_ativo():
				moe.logica(self.__jogador)
				moe.iniciar_animacao_alpha()
			
		if self.__gFase.objetivo_completo():
			if self.__gFase.passar_fase():
				self.__jogador = self.__gFase.reiniciar_fase_atual()
		

	def rodar(self):

		self.__inicializar()
		dt = 0
		while self.__rodando:

			self.__evento()
			self.__atualizar(dt)
			self.__desenhar(dt)

			dt = self.clock.tick(self.fps) / 1000.0

	def __evento(self):

		for e in pygame.event.get():

			if e.type == pygame.QUIT:
				self.__rodando = False

			elif e.type == pygame.MOUSEBUTTONDOWN:

				if e.button == 1:
					pos = pygame.mouse.get_pos()
					print(self.__jogador.y)
					print(self.__jogador.vel_y)
					print(pos[1])
					qnt = pos[1] - self.__jogador.y
					self.__jogador.set_vel_y(pos[1]-600)

			elif e.type == pygame.KEYDOWN:

				if e.key == pygame.K_ESCAPE:
					self.__rodando = False

				if e.key == pygame.K_f:
					if self.mudar_fps:
						self.fps = 30
					else:
						self.fps = 120

					self.mudar_fps = not self.mudar_fps

				if pygame.key.get_mods() & pygame.KMOD_SHIFT and e.key == pygame.K_RETURN:
					if self.__gFase.passar_fase():
						self.__jogador = self.__gFase.reiniciar_fase_atual()
				elif e.key == pygame.K_RETURN:
					self.__jogador.set_y(-1200)

	def __desenhar(self, dt):

		self.__screen.blit(self.__gFase.get_fundo(), (0,0))

		self.__jogador.desenhar(self.__screen, self.camera.aplicar(self.__jogador, dt))


		for plat in self.__gFase.get_plataformas():
			plat.desenhar(self.__screen, self.camera.aplicar(plat, dt))

		for ene in self.__gFase.get_energias():
			ene.desenhar(self.__screen, self.camera.aplicar(ene, dt))

		for ini in self.__gFase.get_inimigos():
			ini.desenhar(self.__screen, self.camera.aplicar(ini, dt), self.camera, dt)

		for moe in self.__gFase.get_moedas():
			moe.desenhar(self.__screen, self.camera.aplicar(moe, dt))

	def __atualizar(self, dt):
		print(self.fps)
		self.__logica(dt)
		self.camera.atualizar(self.__jogador)
		pygame.display.flip()

if __name__ == "__main__":
	jogo = Jogo()
	jogo.rodar()