# @	Não implementado ainda

from dimensao import Dimensao
class Botao(Dimensao):

    def __init__(self, intervalo = 1, ativo = True, visivel = True):

        self.__intervalo = intervalo
        self.__ativo = ativo
        self.__visivel = visivel

    def get_ativo(self):

        return self.__ativo

    def checar_intervalo(self):
    	pass