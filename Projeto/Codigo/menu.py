import pygame
pygame.init()

class Campo(object):

	def __init__(self, texto, cor, pos):
		self.texto = texto
		self.cor = cor
		self.pos = pos

	def desenhar(self, tela, fonte):
		tela.blit(fonte.render(self.texto, True, self.cor), self.pos)

class MenuBase(object):

	def __init__(self, jogo, _id):

		self.fonte = pygame.font.SysFont('Comic Sans MS', 80)
		self.jogo = jogo
		self.tela = jogo.tela
		self.opcao = -1
		self.campos = []
		self.id = _id

	def get_opcao(self):
		return self.opcao

	def get_id(self):
		return self.id

	def desenhar_campos(self):
		for c in self.campos:
			c.desenhar(self.tela, self.fonte)

	def desenhar(self):
		self.tela.fill((0, 0, 0))
		self.desenhar_campos()

	def atualizar(self):
		pygame.display.flip()

	def adicionar_campo(self, texto, cor, pos):
		self.campos.append(Campo(texto, cor, pos))

	def iniciar(self):
		pass

	def remover_campo(self, texto):
		for c in self.campos[:]:
			if c.texto == texto:
				self.campos.remove(c)

	def terminar(self):
		self.campos = []

class MenuInicial(MenuBase):

	def __init__(self, tela):
		super().__init__(tela, 0)

		self.adicionar_campo("Menu Principal", (0,255,255), (200,50))
		self.adicionar_campo("Iniciar jogo", (0,255,255), (200,150))
		self.adicionar_campo("Sair do Jogo", (0,255,255), (200,250))

	def eventos(self):
		for e in pygame.event.get():

			if e.type == pygame.QUIT:
				self.opcao = 1

			if e.type == pygame.KEYDOWN:

				if e.key == pygame.K_ESCAPE:
					self.opcao = 1

			elif e.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()

				if pos[1] > 150 and pos[1] < 230:
					self.opcao = 0

				elif pos[1] > 250 and pos[1] < 330:
					self.opcao = 1				

class MenuTransicao(MenuBase):

	def __init__(self, tela):
		super().__init__(tela, 1)

		self.adicionar_campo("Menu Transição", (0,255,255), (200,50))
		self.adicionar_campo("Proxima Fase", (0,255,255), (200,150))
		self.adicionar_campo("Sair do Jogo", (0,255,255), (200,250))

	def eventos(self):
		for e in pygame.event.get():

			if e.type == pygame.QUIT:
				self.opcao = 1

			if e.type == pygame.KEYDOWN:

				if e.key == pygame.K_ESCAPE:
					self.opcao = 1

			elif e.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()

				if pos[1] > 150 and pos[1] < 230:
					self.opcao = 0

				elif pos[1] > 250 and pos[1] < 330:
					self.opcao = 1

class MenuPausa(MenuBase):

	def __init__(self, tela):
		super().__init__(tela, 2)

		self.adicionar_campo("Menu de Pause", (0,255,255), (200,50))
		self.adicionar_campo("Continuar", (0,255,255), (200,150))
		self.adicionar_campo("Reiniciar Fase", (0,255,255), (200,250))
		self.adicionar_campo("Sair do Jogo", (0,255,255), (200,350))
	
	def eventos(self):
		for e in pygame.event.get():

			if e.type == pygame.QUIT:
				self.opcao = 1

			if e.type == pygame.KEYDOWN:

				if e.key == pygame.K_ESCAPE:
					self.opcao = 0

			elif e.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()

				if pos[1] > 150 and pos[1] < 230:
					self.opcao = 0

				elif pos[1] > 250 and pos[1] < 330:
					self.opcao = 2
					
				elif pos[1] > 350 and pos[1] < 430:
					self.opcao = 1

class MenuFim(MenuBase):

	def __init__(self, tela):
		super().__init__(tela, 3)

		self.adicionar_campo("Fim do Jogo", (0,255,255), (200,50))
		self.adicionar_campo("Recomecar", (0,255,255), (200,150))
		self.adicionar_campo("Sair do Jogo", (0,255,255), (200,350))

	def eventos(self):
		for e in pygame.event.get():

			if e.type == pygame.QUIT:
				self.opcao = 1

			if e.type == pygame.KEYDOWN:

				if e.key == pygame.K_ESCAPE:
					self.opcao = 1

			elif e.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				
				if pos[1] > 150 and pos[1] < 230:
					self.opcao = 2

				elif pos[1] > 350 and pos[1] < 430:
					self.opcao = 1

class Menu(object):

	def __init__(self, tela):

		self.menu_atual = None

		self.menus = (MenuInicial(tela), MenuTransicao(tela), MenuPausa(tela), MenuFim(tela))

	def definir_menu(self, _id):
		for m in self.menus:
			if m.get_id() == _id:
				self.menu_atual = m
				self.logica()
				return

		self.menu_atual = None

	def get_opcao(self):
		return self.menu_atual.get_opcao()

	def logica(self):
		if self.menu_atual:
			while self.menu_atual.get_opcao() == -1:
				self.menu_atual.eventos()
				self.menu_atual.atualizar()
				self.menu_atual.desenhar()

	def restaurar(self):
		if self.menu_atual:
			self.menu_atual.opcao = -1
			self.menu_atual = None

	def get_id_menu_atual(self):
		if self.menu_atual:
			self.menu_atual.get_id()