import os
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Generator, List, Optional

from config import get_config
from sqlmodel import Field, Session, SQLModel, create_engine, delete, select


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str = Field(default='Caçar, evoluir, caçar!')
    email: str = Field(index=True, unique=True)
    senha: str
    classe: str = Field(default='APRENDIZ')
    level: int = Field(default=1)
    experiencia: int = Field(default=0)
    vida: int = Field(default=25)
    energia: int = Field(default=25)
    forca: int = Field(default=1)
    agilidade: int = Field(default=1)
    resistencia: int = Field(default=1)
    inteligencia: int = Field(default=1)
    pontos_disponiveis: int = Field(default=1)
    tamanho_inventario: int = Field(default=1)
    missoes: str = Field(default='')
    data_criacao: datetime = Field(default_factory=lambda: datetime.now())


class UsuarioInventario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(index=True)
    item_nome: str
    quantidade: int = Field(default=1)
    em_uso: bool = Field(default=False)
    data_criacao: datetime = Field(default_factory=lambda: datetime.now())


config = get_config()

engine = create_engine(os.environ.get('DATABASE_URL'), echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, Any, Any]:
    with Session(engine) as session:
        yield session


def criar_usuario(nome: str, email: str, senha: str):
    with get_session() as session:
        session.add(Usuario(
            nome=nome,
            email=email,
            senha=senha
        ))
        session.commit()


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


def create_usuario(nome: str, email: str, senha: str):
    with get_session() as session:
        session.add(Usuario(email=email, senha=senha, nome=nome))
        session.commit()
