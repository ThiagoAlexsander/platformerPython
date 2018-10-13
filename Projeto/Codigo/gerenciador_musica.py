import os
try:
	import glob
except:
	os.system("pip3 install glob --user")
	import glob
from pygame import mixer
import musica

class GerenciadorMusica(object):

	def __init__(self):

		self.lista_de_musicas = []
		mixer.init()
		self.__volume = 0.03

		musicas = glob.glob("../Musica/*.mp3")
		for m in musicas:
			self.lista_de_musicas.append(musica.Musica(m))

	def tocar(self, ID):
		try:
			mixer.music.load(self.lista_de_musicas[ID].diretorio)
			mixer.music.play(-1)
			mixer.music.set_volume(self.__volume)
		except Exception as e:
			mixer.music.stop()

	def parar(self):
		try:
			mixer.music.stop()
		except Exception as ex:
			print(ex)

	def aumentar_volume(self):
		self.__volume += 0.01
		if self.__volume > 1.0:
			self.__volume = 1.0
		mixer.music.set_volume(self.__volume)

	def abaixar_volume(self):
		self.__volume -= 0.01
		if self.__volume < 0.0:
			self.__volume = 0.0
		mixer.music.set_volume(self.__volume)

	def get_volume(self):
		return self.__volume

if __name__ == '__main__':
	obj = GerenciadorMusica()
	obj.iniciar(0)
