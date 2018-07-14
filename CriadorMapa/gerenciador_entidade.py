from os import system
from subprocess import Popen
from shutil import copy2
import pygame

from fase import Fase
try:
	from easygui import enterbox, msgbox, multenterbox
except ImportError:
	from os import system
	system("pip install easygui-0.98.1-py2.py3-none-any.whl --user")
	from sys import exit
	exit()

from jogador import Jogador
from inimigo import Inimigo
from plataforma import Plataforma, PlataformaAndante
from energia import Energia
from moeda import Moeda
from entidade import Entidade

from camera import Camera

class GerenciadorEntidade(object):

	def __init__(self, gf, ff, fase):
		self.fase = fase
		self.gf = gf
		self.ff = ff
		self.camera = Camera(800, 600)
		self.camera_man = Entidade(400, 300)
		self.entidades = []
		self.entidade = None
		self.entidade_copia = None
		self.arrastando_entidade = False
		self.arquivo_atual = ""
		self.mov_x = 0
		self.mov_y = 0
		self.camera_mov_x = self.camera_man.x
		self.camera_mov_y = self.camera_man.y
		self.pos = []
		self.pos_aplicada = []

	def iniciar(self, fase):
		self.fase = fase

	def get_entidades(self):
		return self.entidades

	def organizar_por_camadas(self):
		# TODO: Usar busca binária, pois é melhor que bubble sort
		lista = self.entidades
		for i in lista:
			for j in range(len(lista)-1):
				if lista[j].camada > lista[j+1].camada:
					tmp = lista[j+1]
					lista[j+1] = lista[j]
					lista[j] = tmp

	def copiar_entidade(self, entidade):
		return entidade.clonar()

	def pegar_entidade_cursor(self):
		pos = pygame.mouse.get_pos()
		#pos = self.camera.aplicar_mouse(pos)

		for e in self.entidades:

			if pos[0] > e.x + self.camera.x and pos[0] < e.x + e.w + self.camera.x and \
			   pos[1] > e.y + self.camera.y and pos[1] < e.y + e.h + self.camera.y:
				return e

		return None

	def arrastar_entidade(self, e, pos):
		e.x = pos[0] - self.mov_x
		e.y = pos[1] - self.mov_y

	def get_camera_ref(self):
		return self.camera

	def atualizar(self):
		#jogador = self.gf.get_jogador_ref()
		#if jogador:
		#	self.camera.atualizar(jogador)
		self.camera.atualizar(self.camera_man)	

	def eventos_continuos(self):
		self.pos = pygame.mouse.get_pos()
		self.pos_aplicada = self.camera.aplicar_mouse(self.pos)

		pressionado = pygame.mouse.get_pressed()
		if self.arrastando_entidade:
			self.arrastar_entidade(self.entidade, self.pos_aplicada)

		if pressionado[0]:

			if not self.arrastando_entidade: # Para poder pegar apenas uma entidade.
				self.entidade = self.pegar_entidade_cursor()
				if self.entidade:
					self.mov_x = self.pos_aplicada[0] - self.entidade.x
					self.mov_y = self.pos_aplicada[1] - self.entidade.y
					self.arrastando_entidade = True

		if pressionado[1]:
			#print("pressionado")
			self.camera_man.x = self.camera_mov_x - self.pos[0]
			self.camera_man.y = self.camera_mov_y - self.pos[1]

	def eventos(self, e):

		if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
			self.arrastando_entidade = False

		if e.type == pygame.MOUSEBUTTONDOWN and e.button == 2:
			
			self.camera_mov_x += self.pos[0]
			self.camera_mov_y += self.pos[1]
		
		if e.type == pygame.MOUSEBUTTONUP and e.button == 2:

			self.camera_mov_x -= self.pos[0]
			self.camera_mov_y -= self.pos[1]

		if e.type == pygame.MOUSEBUTTONUP and e.button == 3:
			entidade = self.pegar_entidade_cursor()
			if entidade:					
				
				nomes = entidade.get_nomes()
				param = multenterbox(msg=entidade.__class__.__name__, title='Editor de atributos', fields=(nomes))
				
				if param:
					entidade.setar_atributos(param)
			else:
				nomes = ["ID","Cor", "Imagem Fundo"]
				param = multenterbox(msg="Fase", title='Editor de atributos', fields=(nomes))
				if param:
					self.fase.setar_atributos(param)

		if e.type == pygame.KEYDOWN:

			if e.key == pygame.K_DELETE:
				entidade = self.pegar_entidade_cursor()
				if entidade:
					self.entidades.remove(entidade)
					self.fase.remover(entidade)

			mods = pygame.key.get_mods()
			if mods & pygame.KMOD_CTRL: # get_mods para poder pegar o evento de duas teclas pressionadas (e.g CTRL + NUMPAD1/2/3/4)

				if mods & pygame.KMOD_SHIFT and e.key == pygame.K_s:
					if self.arquivo_atual:
						self.ff.salvar_arquivo("Fases/"+self.arquivo_atual, self.fase)
						print("Salvo!")
					else:
						msgbox("Nenhum arquivo foi aberto!", "Erro")
				elif e.key == pygame.K_s:
					if self.fase.get_id() == -1:
						_id = enterbox("Digite o id da fase!")
						if _id:
							self.fase.set_id(_id)
						else:
							return
					
					arquivo = enterbox("Digite o nome do arquivo a ser salvo!")
					if arquivo:
						self.arquivo_atual = arquivo
						self.ff.salvar_arquivo("Fases/"+self.arquivo_atual, self.fase)

				if e.key == pygame.K_1:
					jogador = Jogador(400,420,30,30,0.0,0.0,2.3,(0,25,125),"no_img")
					self.entidades.append(jogador)
					self.fase.set_jogador(jogador)

				elif e.key == pygame.K_2:
					plataforma = Plataforma(0,570,800,30,0.0,0.0,0.0,(10,10,15), "no_img")
					self.entidades.append(plataforma)
					self.fase.adicionar_plataforma(plataforma)

				elif e.key == pygame.K_3:
					plataforma = PlataformaAndante(400,300,100,30,0,0,0.5,(100,200),(0,0),0.0,(200,0,150),"no_img")
					self.entidades.append(plataforma)
					self.fase.adicionar_plataforma(plataforma)

				elif e.key == pygame.K_4:
					energia = Energia(400,240,20,30,0,0,0.0,True,(255,255,125),"no_img")
					self.entidades.append(energia)
					self.fase.adicionar_energia(energia)

				elif e.key == pygame.K_5:
					moeda = Moeda(300,510,10,10,0,0,0.0,(255,100,10),"no_img")
					self.entidades.append(moeda)
					self.fase.adicionar_moeda(moeda)

				elif e.key == pygame.K_6:
					inimigo = Inimigo(170,540,30,30,0,0,2.0,True,25.0,False,(0,25,125),"canon.png","gold_bullet.png")
					self.entidades.append(inimigo)
					self.fase.adicionar_inimigo(inimigo)

				elif e.key == pygame.K_l:
					arquivo = enterbox("Digite o nome do arquivo a ser carregado!")
					if arquivo:
						self.arquivo_atual = arquivo
						ret = self.gf.iniciar(self.arquivo_atual)
						if ret:
							ret = ret[:]
							self.entidades = ret[0]
							self.fase = ret[1]
						else:
							msgbox("Arquivo não existente ou corrompido!", "Erro")

				elif e.key == pygame.K_c:
					entidade = self.pegar_entidade_cursor()
					if entidade:
						self.entidade_copia = self.copiar_entidade(entidade)
				
				elif e.key == pygame.K_v:
					if self.entidade_copia:
						self.entidade_copia.x = self.pos[0] - self.camera.x - self.entidade_copia.w / 2
						self.entidade_copia.y = self.pos[1] - self.camera.y - self.entidade_copia.h / 2
						clone = self.copiar_entidade(self.entidade_copia)
						self.entidades.append(clone)
						self.fase.adicionar(clone)

				elif mods & pygame.KMOD_SHIFT and e.key == pygame.K_f:
					if self.arquivo_atual:
						copy2("Fases/"+self.arquivo_atual, "../Projeto/Fases")
						print("Arquivo enviado!")
					else:
						msgbox("Nenhum arquivo para ser enviado!", "Erro")

				elif e.key == pygame.K_f:
					nome = enterbox("Digite o nome do arquivo a enviado!")
					if nome:
						copy2("Fases/"+nome, "../Projeto/Fases")						

				elif mods & pygame.KMOD_SHIFT and e.key == pygame.K_b:
					if self.arquivo_atual:
						self.ff.salvar_arquivo("Fases/"+self.arquivo_atual, self.fase)
						print("Salvo!")
						copy2("Fases/"+self.arquivo_atual,"../Projeto/Fases")
						print("Arquivo enviado!")
						Popen("python jogo.py", cwd="../Projeto/Codigo/", shell=True)
					else:
						msgbox("Nenhum arquivo aberto ou salvo!", "Erro")

				elif e.key == pygame.K_b:
					Popen("python jogo.py", cwd="../Projeto/Codigo/", shell=True)

				elif e.key == pygame.K_n:
					self.entidades = []
					self.fase = Fase(-1, None, self.dummy_fundo, [], [], [], [], "no_img")
					self.arquivo_atual = ""

"""
def retirar_valores(self, lista, valor):
		nova_lista = []
		for i in lista:
			if i != valor:
				nova_lista.append(i)
		return nova_lista
		
"""