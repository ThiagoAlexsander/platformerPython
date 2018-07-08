import pygame

class Sprite(object):

	def __init__(self, imagem = None, cor = (255, 255, 255), _min = 0, _max = 255, multiplicador = 1.0):

		self.caminho_imagem = imagem
		self.imagem = None
		self.cor = cor
		self.max = _max
		self.min = _min
		self.multiplicador = 1.0
		self.contador = self.min + self.multiplicador

	def get_imagem(self):
		return self.imagem

	def inicializar(self):
		
		if self.caminho_imagem and not "no_img" in self.caminho_imagem:
			self.imagem = pygame.image.load("../Imagens/"+self.caminho_imagem)
			self.imagem.set_colorkey((255, 0, 255))
			self.imagem.convert_alpha()		
		
		else:
			self.imagem = pygame.Surface((self.w, self.h))
			self.imagem.fill(self.cor)

	def iniciar_animacao_alpha(self):
		
		if not self.imagem:
			self.inicializar()
		
		if self.contador < self.min or self.contador > self.max:
			
			self.multiplicador = -self.multiplicador
		
		self.contador += self.multiplicador
		self.imagem.set_alpha(self.contador)

	def parar_animacao_alpha(self):
		pass