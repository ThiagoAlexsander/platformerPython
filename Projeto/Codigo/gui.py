import pygame

class Caixa(object):

	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.dimensao = pygame.Surface((w, h))

	def get_rect(self):
		return self.dimensao

	def get_pos(self):
		return (self.x, self.y)

class Texto(Caixa):

	def __init__(self):
		pass

	def desenhar(self):
		pass

class GUI(object):

	def __init__(self, tipo, x, y, w, h, cor):

		self.caixa = Caixa(x, y, w, h)
		self.cor = cor
		self.tipo = tipo

	def desenhar(self, caixa):

		if caixa:
			rect = self.caixa.get_rect()
			rect.set_alpha(10)
			caixa.blit(rect, self.caixa.get_pos())
		else:
			print("Objeto da caixa esta vazia!")

	def desenhar_componentes(self):
		for c in self.componentes:
			c.desenhar()

	def adicionar_texto(self, x, y, w, h, texto):

		pass