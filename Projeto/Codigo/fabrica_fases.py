from fase import Fase
from jogador import Jogador
from energia import Energia
from inimigo import Inimigo
from moeda import Moeda
from plataforma import Plataforma, PlataformaAndante
import pygame

pygame.init()
pygame.display.set_mode((800, 600))

def parse_tuple(string):
	try:
		s = eval(str(string))
		if type(s) == tuple:
			return s
		return
	except:
		return

def parse_bool(string):
	return not (string.lower() == "0" or string.lower() == "false")

class FabricaFases(object):

	def carregar_arquivo(self, caminho):

		f = open(caminho, "r")
		conteudo = f.readlines()
		f.close()
		info = []
		for linha in conteudo:
			
			linha = linha.split(";")
			info += linha
		
		return info

	def criar_fase(self, linha):
		plataformas = []
		moedas = []
		energias = []
		inimigos = []
		cor = (65, 65, 65)
		fundo = pygame.Surface((800, 600))
		fundo.fill(cor)
		jogador = None
		_id = 0
		for i in linha:
			
			i = i.split(":")
			
			if i[0] == "plataforma":
				i = i[1].split("|")
				print(i)
				plataformas.append(Plataforma(float(i[0]), float(i[1]), float(i[2]), float(i[3]), float(i[4]), float(i[5]), float(i[6]), parse_tuple(i[7]), i[8]))

			elif i[0] == "plataforma_andante":
				i = i[1].split("|")
				print(i)
				plataformas.append(PlataformaAndante(float(i[0]), float(i[1]), float(i[2]), float(i[3]), float(i[4]), float(i[5]), float(i[6]), parse_tuple(i[7]), parse_tuple(i[8]), float(i[9]), parse_tuple(i[10]), i[11]))

			elif i[0] == "energia":
				i = i[1].split("|")
				print(i)
				energias.append(Energia(float(i[0]), float(i[1]), float(i[2]), float(i[3]), float(i[4]), float(i[5]), float(i[6]), parse_bool(i[7]), parse_tuple(i[8]), i[9]))

			elif i[0] == "inimigo":
				i = i[1].split("|")
				print(i)
				inimigos.append(Inimigo(float(i[0]), float(i[1]), float(i[2]), float(i[3]), float(i[4]), float(i[5]), float(i[6]), parse_bool(i[7]), float(i[8]), parse_bool(i[9]), parse_tuple(i[10]), i[11], i[12]))

			elif i[0] == "jogador":
				i = i[1].split("|")

				jogador = Jogador(float(i[0]), float(i[1]), float(i[2]), float(i[3]), float(i[4]), float(i[5]), float(i[6]), parse_tuple(i[7]), i[8])

			elif i[0] == "moeda":
				i = i[1].split("|")

				moedas.append(Moeda(float(i[0]), float(i[1]), float(i[2]), float(i[3]), float(i[4]), float(i[5]), float(i[6]), parse_tuple(i[7]), i[8]))

			elif i[0] == "cor":
				cor = parse_tuple(i[1])
				fundo.fill(cor)

			elif i[0] == "fundo":
				caminho_fundo = i[1]

			elif i[0] == "fase_indice":
				_id = int(i[1])

		if caminho_fundo != "no_img":
			fundo = pygame.image.load("../Imagens/"+caminho_fundo).convert_alpha()

		return Fase(_id, jogador, fundo, plataformas, moedas, energias, inimigos, cor)

if __name__ == "__main__":

	fb = FabricaFases()
	arquivo = fb.carregar_arquivo("../Fases/fase1.gload")
	fase = fb.criar_fase(arquivo)
	print(fase.get_cor())
	plataformas = fase.get_inimigos()
	sur = pygame.display.set_mode((800, 600)) 
	plataformas[0].desenhar(sur)
	