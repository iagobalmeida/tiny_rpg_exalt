from models.entidade import OBJETOS_TIPOS, Entidade


class Inimigo(Entidade):
    tipo: OBJETOS_TIPOS = 'INIMIGO'
    sprite_particula: str
