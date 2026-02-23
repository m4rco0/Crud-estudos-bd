"""
Schemas de tabelas usados para fazer a API
"""

from decimal import Decimal

from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


# ----- Esquemas do Cliente


class ClienteSchema(BaseModel):
    nome: str
    email: EmailStr
    cpf: str
    senha: str


class PublicClient(BaseModel):
    idcliente: int
    nome: str
    email: EmailStr


class ClienteDB(ClienteSchema):
    id: int


# ------- Esquemas de Lojas


class LojasSchema(BaseModel):
    nome: str
    email: EmailStr
    qtsvendas: int
    ganhoVendas: Decimal
    cnpj: str


class PublicLojas(BaseModel):
    idlojas: int
    nome: str
    email: EmailStr


class LojasDB(LojasSchema):
    id: int


# ----------- Esquema de Produto


class ProdutoSchema(BaseModel):
    nome: str
    preco: Decimal


class ProdutoDB(ProdutoSchema):
    id: int


# ----------- Esquema de  Estoque


class EstoqueSchema(BaseModel):
    disponivel: int


class EstoquePublic(EstoqueSchema):
    id_produto: int


# -------- Esquema em listas ---------
class LojasList(BaseModel):
    lojas: list[PublicLojas]


class ProdutoList(BaseModel):
    produtos: list[ProdutoDB]


class ClienteList(BaseModel):
    clientes: list[PublicClient]
