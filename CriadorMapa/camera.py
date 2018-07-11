class Camera(object):

	def __init__(self, largura, altura):

		self.x = 0
		self.y = 0
		self.w = largura
		self.h = altura
		self.largura = largura
		self.altura = altura

	def aplicar(self, entidade, dt):
		x = entidade.x
		y = entidade.y
		x += self.x + dt * 2
		y += self.y + dt * 2
		return (x, y)

	def aplicar_mouse(self, pos):
		xy = list(pos)
		xy[0] += self.x
		xy[1] += self.y
		return xy

	def atualizar(self, foco):
		# print(foco.x)
		# print(foco.y)
		self.x = -foco.x + int(self.largura / 2)
		self.y = -foco.y + int(self.altura / 2)