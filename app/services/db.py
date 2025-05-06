import os
import threading
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Generator, List, Optional, Tuple

from cachetools import TTLCache
from config import get_config
from data.missoes import MISSOES, missoes_dict_to_json
from pydantic import BaseModel
from sqlmodel import (Field, Session, SQLModel, create_engine, delete, select,
                      text)

CACHE = TTLCache(maxsize=100, ttl=60)
CACHE_LOCK = threading.Lock()


class LeaderboardEntry(BaseModel):
    id: int
    nome: str
    level: int
    posicao: int
    classe: str
    forca: int
    agilidade: int
    resistencia: int
    inteligencia: int


def usuario_patrocinio_expiracao():
    return datetime.now()


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(default=None)
    descricao: str = Field(default='Caçar, evoluir, caçar!')
    email: str = Field(index=True, unique=True)
    senha: str = Field(default=None)
    patrocinador: bool = Field(default=False)
    patrocinio_expiracao: datetime = Field(default_factory=usuario_patrocinio_expiracao)
    ouro: int = Field(default=0)
    classe: str = Field(default='FAZENDEIRO')
    level: int = Field(default=1)
    experiencia: int = Field(default=0)
    vida: int = Field(default=25)
    vida_maxima: int = Field(default=25)
    energia: int = Field(default=25)
    energia_maxima: int = Field(default=25)
    forca: int = Field(default=1)
    agilidade: int = Field(default=1)
    resistencia: int = Field(default=1)
    inteligencia: int = Field(default=1)
    pontos_disponiveis: int = Field(default=1)
    tamanho_inventario: int = Field(default=8)
    missoes: str = Field(default=missoes_dict_to_json(MISSOES))
    data_criacao: datetime = Field(default_factory=lambda: datetime.now())


class UsuarioInventario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(index=True)
    item_nome: str
    quantidade: int = Field(default=1)
    em_uso: bool = Field(default=False)
    data_criacao: datetime = Field(default_factory=lambda: datetime.now())


config = get_config()

engine = create_engine(os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/tinyrpg'), echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def reset_db():
    SQLModel.metadata.drop_all(engine)
    create_db_and_tables()


@contextmanager
def get_session() -> Generator[Session, Any, Any]:
    with Session(engine) as session:
        yield session


def __criar_usuario(nome: str, email: str, senha: str, **kwargs):
    try:
        with get_session() as session:
            session.add(Usuario(
                nome=nome,
                email=email,
                senha=senha,
                **kwargs
            ))
            session.commit()
    except Exception as ex:
        pass


def __criar_usuario_de_teste(classe: str, level: int = 16):
    missoes = MISSOES
    if level > 16:
        missoes = {**MISSOES}
        for nome_regiao in missoes:
            missoes[nome_regiao]['completa'] = True

    __criar_usuario(
        nome=f'{classe.title()} Teste',
        email=f'{classe.lower()}@teste.com',
        senha='teste',
        classe=classe,
        level=level,
        vida=level*5,
        vida_maxima=level*5,
        energia=level*5,
        energia_maxima=level*5,
        forca=int(level*3/4),
        resistencia=int(level*3/4),
        agilidade=int(level*3/4),
        inteligencia=int(level*3/4),
        tamanho_inventario=64,
        missoes=missoes_dict_to_json(missoes)
    )


def criar_usuarios_de_teste():
    __criar_usuario_de_teste('INICIANTE', 16)
    __criar_usuario_de_teste('VIGIA', 32)
    __criar_usuario_de_teste('GUARDIAO', 64)
    __criar_usuario_de_teste('PALADINO', 128)
    __criar_usuario_de_teste('APRENDIZ', 16)
    __criar_usuario_de_teste('MAGO', 32)
    __criar_usuario_de_teste('FEITICEIRO', 64)
    __criar_usuario_de_teste('ARCANO', 128)
    __criar_usuario_de_teste('SELVAGEM', 16)
    __criar_usuario_de_teste('BARBARO', 32)
    __criar_usuario_de_teste('BERSERKER', 64)
    __criar_usuario_de_teste('CAMPEAO', 128)
    __criar_usuario_de_teste('VAGABUNDO', 16)
    __criar_usuario_de_teste('LADINO', 32)
    __criar_usuario_de_teste('ASSASSINO', 64)
    __criar_usuario_de_teste('PREDADOR', 128)
    level = 256
    missoes = {**MISSOES}
    for nome_regiao in missoes:
        missoes[nome_regiao]['completa'] = True
    __criar_usuario(
        nome=f'AMON Beats',
        email=f'amonbeats@teste.com',
        senha='teste',
        classe='CAMPEAO',
        level=level,
        vida=level*5,
        vida_maxima=level*5,
        energia=level*5,
        energia_maxima=level*5,
        forca=int(level*3/4),
        resistencia=int(level*3/4),
        agilidade=int(level*3/4),
        inteligencia=int(level*3/4),
        tamanho_inventario=64,
        missoes=missoes_dict_to_json(missoes)
    )


def get_usuario_by_email(email: str) -> Usuario:
    with get_session() as session:
        return session.exec(select(Usuario).where(Usuario.email == email)).first()


def update_usuario(usuario_id: int, valores: dict):
    with get_session() as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise ValueError(f'Usuário com id {usuario_id} não encontrado')
        usuario.sqlmodel_update(valores)
        session.commit()


def get_inventario_by_usuario_id(usuario_id: int) -> List[UsuarioInventario]:
    with get_session() as session:
        return session.exec(select(UsuarioInventario).where(UsuarioInventario.usuario_id == usuario_id)).all()
        # return session.exec(select(UsuarioInventario)).all()


def update_inventario_by_usuario_id(usuario_id: int, inventario: List[UsuarioInventario]):
    with get_session() as session:
        session.exec(delete(UsuarioInventario).where(UsuarioInventario.usuario_id == usuario_id))
        for item in inventario:
            session.add(item)
            session.commit()


def create_usuario(email: str, nome: str = None, senha: str = None) -> Usuario:
    with get_session() as session:
        entidade = Usuario(email=email, senha=senha, nome=nome)
        session.add(entidade)
        session.commit()
        session.refresh(entidade)
        return entidade


def get_placar_de_lideres(usuario_id: int = None) -> List[LeaderboardEntry]:
    key: Tuple[int] = (usuario_id,) if usuario_id else ('*',)

    with CACHE_LOCK:
        if key in CACHE:
            return CACHE[key]

    resultado = []

    with get_session() as session:
        query = text(f"""
            WITH leaderboard AS (
                SELECT id, nome, level, classe, forca, agilidade, resistencia, inteligencia,
                    ROW_NUMBER() OVER (ORDER BY level DESC, id ASC) AS posicao
                FROM usuario WHERE email NOT LIKE '%teste%'
            )
            SELECT *
            FROM leaderboard
            WHERE posicao <= 25 {'OR id = :usuario_id' if usuario_id else ''};
        """)
        result = session.exec(query, params={"usuario_id": usuario_id}) if usuario_id else session.exec(query)
        rows = result.fetchall()
        resultado = [LeaderboardEntry(**row._mapping) for row in rows]

    if resultado:
        with CACHE_LOCK:
            CACHE[key] = resultado

    return resultado
