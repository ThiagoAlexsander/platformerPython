from entidade import Entidade
from sprite import Sprite
class Aprimoramento(Entidade, Sprite):

    def __init__(self, ativo = False, tipo = "Default"):

        self.__ativo = ativo
        self.__tipo = tipo
