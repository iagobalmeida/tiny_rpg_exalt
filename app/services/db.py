import os
from datetime import datetime
from typing import Annotated, List

from config import get_config
from fastapi import Depends
from models.jogador import CLASSE_TIPOS
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(index=True)
    senha: str
    nivel: int = Field(default=1)
    experiencia: int = Field(default=0)
    classe: CLASSE_TIPOS = Field(default='APRENDIZ')
    level: int = Field(default=1)
    forca: int = Field(default=1)
    agilidade: int = Field(default=1)
    resistencia: int = Field(default=1)
    inteligencia: int = Field(default=1)
    pontos_disponiveis: int = Field(default=1)
    tamanho_inventario: int = Field(default=1)
    missoes: str = Field(default='')
    data_criacao: datetime = Field(default_factory=datetime.now())


class UsuarioInventario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(index=True)
    item_nome: str
    quantidade: int = Field(default=1)
    data_criacao: datetime = Field(default_factory=datetime.now())


config = get_config()
connect_args = {"check_same_thread": False}

engine = create_engine(os.environ.get('DATABASE_URL'), connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def get_usuario_by_email(email: str, session: Session = Depends(get_session)) -> Usuario:
    return session.exec(select(Usuario).where(Usuario.email == email)).first()


def get_inventario_by_usuario_id(usuario_id: int, session: Session = Depends(get_session)) -> List[UsuarioInventario]:
    return session.exec(select(UsuarioInventario).where(UsuarioInventario.usuario_id == usuario_id)).all()


SessionDep = Annotated[Session, Depends(get_session)]
