import pygame
from gerenciador_fase import GerenciadorFase

class EditorFases(object):

	def __init__(self):

		pygame.init()
		pygame.font.init()

		self.tela = pygame.display.set_mode((800, 600))
		self.clock = pygame.time.Clock()
		self.rodando = False
		self.gf = GerenciadorFase()
		self.ff = self.gf.get_fabrica_fases()
		self.ge = self.gf.get_gerenciador_entidades()
		self.camera = self.ge.get_camera_ref()


		"""
			self.fonte = pygame.font.match_font("Arial")
			self.entidades = []
			self.entidade = None
			self.entidade_copia = None
			self.arrastando_entidade = False
			self.mov_x = 0
			self.mov_y = 0
			self.arquivo_atual = ""
		"""

	def sair(self):
		self.rodando = False

	def desenhar_entidades(self, dt):

		#if self.gf.get_fase_atual():
		#	print(self.gf.get_fase_atual().get_caminho_fundo())
		self.gf.desenhar_fundo(self.tela)
			#print(self.gf.get_caminho_fundo())
			#self.tela.blit(self.gf.get_fundo(), (0, 0))

		self.ge.organizar_por_camadas()

		for e in self.ge.get_entidades():
			try:
				if not e.__class__.__name__ == "Inimigo":
					e.desenhar(self.tela, self.camera.aplicar(e, 0))
				else:
					e.desenhar(self.tela, self.camera.aplicar(e, 0), self.camera, 0)
			except:
				print(e.__class__.__name__)


	def eventos(self):
		
		self.ge.eventos_continuos()

		for e in pygame.event.get():

			self.ge.eventos(e)

			if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				self.rodando = False
				

	def desenhar(self, dt):

		self.desenhar_entidades(dt)

	def atualizar(self):

		self.ge.atualizar() # Atualizar camera
		pygame.display.flip()

	def novo(self):

		self.rodar()

	def rodar(self):

		self.rodando = True
		dt = 0
		while self.rodando:


			self.eventos()
			self.atualizar()
			self.desenhar(dt)
			dt = self.clock.tick(60)

if __name__ == "__main__":

	m = EditorFases()

	m.novo()