class Entidade(object):

	def __init__(self, x = 30, y = 30, w = 30, h = 30, vel_x = 0, vel_y = 0, vel = 1):

		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.vel = vel

	def get_posicao_inicial(self):
		return (self.x, self.y)

	def aplicar_posicao_x(self, vel):
		self.x += vel

	def aplicar_posicao_y(self, vel):
		self.y += vel

	def colidindo_esquerda(self, e):
		return self.x + self.w + self.vel_x > e.x + e.vel_x and \
		   self.x + self.w < e.x and \
		   self.y + self.h > e.y and \
		   self.y < e.y + e.h
	
	def colidindo_direita(self, e):
		return self.x + self.vel_x < e.x + e.w + e.vel_x and \
		   self.x > e.x + e.w and \
		   self.y + self.h > e.y and \
		   self.y < e.y + e.h

	def colidindo_cima(self, e):
		return self.y + self.h + self.vel_y > e.y + e.vel_y and \
		   self.y < e.y and \
		   self.x + self.w > e.x and \
		   self.x < e.x + e.w

	def colidindo_baixo(self, e):
		return self.y + self.vel_y < e.y + e.h and \
		   self.y + self.h > e.y + e.h + e.vel_y and \
		   self.x + self.w > e.x and \
		   self.x < e.x + e.w

	def colidindo(self, e):
		return self.x + self.w + self.vel_x > e.x and self.x - self.vel_x < e.x + e.w and \
			   self.y + self.h + self.vel_y > e.y and self.y - self.vel_y < e.y + e.h

	def set_x(self, x):
		self.x = x

	def set_y(self, y):
		self.y = y

	def set_vel_x(self, vel_x):
		self.vel_x = vel_x

	def set_vel_y(self, vel_y):
		self.vel_y = vel_y

	def set_vel(self, vel):
		self.vel = vel

	def get_esquerda(self):
		return self.x

	def get_direita(self):
		return self.x + self.w

	def get_cima(self):
		return self.y

	def get_baixo(self):
		return self.y + self.h

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_w(self):
		return self.w

	def get_h(self):
		return self.h

	def get_vel_x(self):
		return self.vel_x

	def get_vel_y(self):
		return self.vel_y

	def get_vel(self):
		return self.vel

	def set_pos(self, pos):
		self.x = pos[0]
		self.y = pos[1]