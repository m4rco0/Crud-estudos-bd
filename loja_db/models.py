from decimal import Decimal

from sqlalchemy import DECIMAL, ForeignKey, Integer, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    registry,
    relationship,
)

table_registry = registry()


class Base(DeclarativeBase):
    registry = table_registry


class Cliente(Base):
    __tablename__ = 'cliente'
    __table_args__ = {'schema': 'db_loja'}

    idcliente: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(45))
    email: Mapped[str] = mapped_column(String(45), unique=True)
    cpf: Mapped[str] = mapped_column(String(45), unique=True)
    senha: Mapped[str] = mapped_column(String(45))


class Lojas(Base):
    __tablename__ = 'lojas'
    __table_args__ = {'schema': 'db_loja'}

    idlojas: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(45))
    email: Mapped[str] = mapped_column(String(45), unique=True)
    qtsvendas: Mapped[int] = mapped_column(Integer)
    ganhoVendas: Mapped[Decimal] = mapped_column('ganhovendas', DECIMAL(10, 3))
    cnpj: Mapped[str] = mapped_column(String(45), unique=True)


class Produto(Base):
    __tablename__ = 'produto'
    __table_args__ = {'schema': 'db_loja'}

    idProduto: Mapped[int] = mapped_column('idproduto', primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(45))
    preco: Mapped[Decimal] = mapped_column('preço')

    estoque: Mapped['Estoque'] = relationship(
        'Estoque', back_populates='produto', uselist=False, cascade="all, delete-orphan"
    )


class Estoque(Base):
    __tablename__ = 'estoque'
    __table_args__ = {'schema': 'db_loja'}

    id_produto: Mapped[int] = mapped_column(
        'produto_idproduto',
        ForeignKey('db_loja.produto.idproduto'),
        primary_key=True,
    )

    disponivel: Mapped[int] = mapped_column(Integer, default=0)

    produto: Mapped['Produto'] = relationship(
        'Produto', back_populates='estoque'
    )
