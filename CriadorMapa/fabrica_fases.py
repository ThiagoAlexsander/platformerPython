from fase import Fase
from jogador import Jogador
from energia import Energia
from inimigo import Inimigo
from moeda import Moeda
from plataforma import Plataforma, PlataformaAndante
import pygame

def parse_tuple(string):
	try:
		s = eval(str(string))
		if type(s) == tuple:
			return s
		return
	except:
		return

def parse_bool(string):
	try:
		s = eval(str(string))
		if type(s) == bool:
			return s
		return
	except:
		return

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

	def salvar_arquivo(self, caminho, fase):

		f = open(caminho, "w")
		
		conteudo = []

		# Primeiro se faz um append baseado nos atributos da fase.

		conteudo.append(
			"fase_indice:"+str(fase.get_id())+";"+
			"fundo:"+str(fase.get_caminho_fundo())+";"
			"cor:"+str(fase.get_cor())+";"
		)

		# E depois baseado nas entidades da fase.

		for plat in fase.get_plataformas():
			conteudo.append(plat.get_tipo()+":")
			for info in plat.get_info():
				conteudo.append(info)
				conteudo.append("|")
			conteudo = conteudo[:-1]
			conteudo.append(";")


		for moe in fase.get_moedas():
			conteudo.append("moeda:")
			for info in moe.get_info():
				conteudo.append(info)
				conteudo.append("|")
			conteudo = conteudo[:-1]
			conteudo.append(";")

		for ene in fase.get_energias():
			conteudo.append("energia:")
			for info in ene.get_info():
				conteudo.append(info)
				conteudo.append("|")
			conteudo = conteudo[:-1]
			conteudo.append(";")

		for ini in fase.get_inimigos():
			conteudo.append("inimigo:")
			for info in ini.get_info():
				conteudo.append(info)
				conteudo.append("|")
			conteudo = conteudo[:-1]
			conteudo.append(";")

		if fase.get_jogador_ref():
			conteudo.append("jogador:")
			for info in fase.get_jogador().get_info():
				conteudo.append(info)
				conteudo.append("|")
			conteudo = conteudo[:-1]
			conteudo.append(";")

		f.writelines(conteudo)

		f.close()

		#return conteudo

	def criar_fase(self, linha):

		plataformas = []
		moedas = []
		energias = []
		inimigos = []
		cor = (65, 65, 65)
		caminho_fundo = "no_img"
		fundo = pygame.Surface((800, 600))
		#print(id(fundo))
		fundo.fill(cor)
		jogador = None
		_id = 0
		for i in linha:
			
			i = i.split(":")
			
			if i[0] == "plataforma":
				i = i[1].split("|")
				
				plataformas.append(Plataforma(float(i[0]), float(i[1]), float(i[2]), float(i[3]), float(i[4]), float(i[5]), float(i[6]), parse_tuple(i[7]), i[8]))

			elif i[0] == "plataforma_andante":
				i = i[1].split("|")
				
				plataformas.append(PlataformaAndante(float(i[0]), float(i[1]), float(i[2]), float(i[3]), float(i[4]), float(i[5]), float(i[6]), parse_tuple(i[7]), parse_tuple(i[8]), float(i[9]), parse_tuple(i[10]), i[11]))

			elif i[0] == "energia":
				i = i[1].split("|")
				
				energias.append(Energia(float(i[0]), float(i[1]), float(i[2]), float(i[3]), float(i[4]), float(i[5]), float(i[6]), True, parse_tuple(i[8]), i[9]))

			elif i[0] == "inimigo":
				i = i[1].split("|")
				inimigos.append(Inimigo(float(i[0]), float(i[1]), float(i[2]), float(i[3]), float(i[4]), float(i[5]), float(i[6]), i[7], float(i[8]), parse_bool(i[9]), parse_tuple(i[10]), i[11], i[12]))

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
			fundo = pygame.image.load("Imagens/"+caminho_fundo).convert_alpha()

		return Fase(_id, jogador, fundo, plataformas, moedas, energias, inimigos, caminho_fundo, cor)

if __name__ == "__main__":


	pygame.init()
	screen = pygame.display.set_mode((800, 600))

	fb = FabricaFases()
	#arquivo = fb.carregar_arquivo("fase2.gload")
	#fase = fb.criar_fase(arquivo)
	#print(fase.get_jogador().get_info())
	#fb.salvar_arquivo("teixte.gload", fase)
	arquivo = fb.carregar_arquivo("Fases/fase1.gload")
	fase = fb.criar_fase(arquivo)


	running = True
	while running:
		for e in pygame.event.get():
			if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				running = False

		screen.blit(fase.get_fundo(), (0, 0))
		pygame.display.update()
	inimigos = fase.get_inimigos()

	