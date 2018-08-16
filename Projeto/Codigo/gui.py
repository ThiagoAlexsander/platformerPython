import pygame

class Caixa(object):

	def __init__(self, x, y, w, h, cor, transparencia = 255):

		self.tela = pygame.Surface((w, h))
		self.tela.fill(cor)
		self.tela.set_alpha(transparencia)	
		self.rect = self.tela.get_rect()
		self.rect.x = x
		self.rect.y = y

	def get_superficie(self):
		return self.tela

	def get_pos(self):
		return [self.rect.x, self.rect.y]

	def definir_transparencia(self, valor):
		self.tela.set_alpha(valor)

class Texto(object):

	def __init__(self, tamanho, gui_w, x, y, w, h, texto, transparencia, cor_texto, cor_superficie):

		pygame.font.init()

		self.fonte = pygame.font.SysFont('Comic Sans MS', tamanho)
		self.caixa = Caixa(x, y, gui_w, tamanho, cor_superficie, transparencia)
		self.texto = texto
		self.cor = cor_texto

	def definir_texto(self, texto):
		self.texto = texto

	def desenhar(self, superficie):

		superficie.blit(self.caixa.get_superficie(), self.caixa.get_pos())
		superficie_texto = self.fonte.render(self.texto, False, self.cor)
		pos = self.caixa.get_pos()
		pos[1] -= 3
		superficie.blit(superficie_texto, pos)


class GerenciadorTexto(object):

	def __init__(self):
		self.__lista_textos = []

	def desenhar(self, superficie):

		for c in self.__lista_textos:
			c.desenhar(superficie)

	def adicionar_texto(self, tamanho, gui_w, x, y, w, h, texto, transparencia, cor_texto, cor_superficie):

		self.__lista_textos.append(Texto(tamanho, gui_w, x, y, w, h, texto, transparencia, cor_texto, cor_superficie))

	def definir_texto(self, indice, texto):
		for i in range(len(self.__lista_textos)):
			if indice == i:
				self.__lista_textos[i].definir_texto(texto)

class GUI(object):

	def __init__(self, x, y, w, h, cor, transparencia = 255):

		self.caixa = Caixa(x, y, w, h, cor, transparencia)
		self.__g_t = GerenciadorTexto()

	def definir_transparencia(self, valor):
		self.caixa.definir_transparencia(valor)

	def desenhar(self, superficie):

		if superficie:
			
			superficie.blit(self.caixa.get_superficie(), self.caixa.get_pos())
			self.__desenhar_componentes(superficie)

		else:
			print("Falha ao desenhar HUD!")

	def __desenhar_componentes(self, superficie):

		self.__g_t.desenhar(superficie)

	def adicionar_texto(self, tamanho, x, y, w, h, texto, transparencia = 255, cor_texto = (255, 255, 255), cor_superficie = (255, 10, 10) ):

		if x > self.caixa.rect.x + self.caixa.rect.w:
			x = self.caixa.rect.x + self.caixa.rect.w
		elif x < self.caixa.rect.x:
			x = self.caixa.rect.x

		if y > self.caixa.rect.y + self.caixa.rect.h:
			y = self.caixa.rect.y + self.caixa.rect.h
		elif y < self.caixa.rect.y:
			y = self.caixa.rect.y

		if texto:
			self.__g_t.adicionar_texto(tamanho, self.caixa.rect.w, x, y, w, h, str(texto), transparencia, cor_texto, cor_superficie)
		else:
			self.__g_t.adicionar_texto(tamanho, self.caixa.rect.w, x, y, w, h, "Unknown", transparencia, cor_texto, cor_superficie)

	def definir_texto(self, indice, texto):
		self.__g_t.definir_texto(indice, texto)