"""Configuração de rotas do fastapi"""

from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from loja_db.database import get_session
from loja_db.models import Cliente, Estoque, Lojas, Produto
from loja_db.schemas import (
    ClienteList,
    ClienteSchema,
    EstoquePublic,
    LojasList,
    LojasSchema,
    Message,
    ProdutoSchema,
    PublicClient,
    PublicLojas,
)

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hello, world!'}


@app.post(
    '/users/', status_code=HTTPStatus.CREATED, response_model=PublicClient
)
def create_cliente(
    cliente: ClienteSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(
        select(Cliente).where(
            (Cliente.email == cliente.email) | (Cliente.cpf == cliente.cpf)
        )
    )

    if db_user:
        if cliente.email == db_user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='email já cadastrado!'
            )
        elif cliente.cpf == db_user.cpf:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='CPF já cadastrado!'
            )

    new_user = Cliente(
        nome=cliente.nome,
        email=cliente.email,
        cpf=cliente.cpf,
        senha=cliente.senha,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


""" Rota para pegar todos os usuarios do BD"""


@app.get('/users/', status_code=HTTPStatus.OK, response_model=ClienteList)
def read_clientes(session: Session = Depends(get_session)):

    clientes = session.scalars(select(Cliente)).all()
    return {'clientes': clientes}


""" Rota para pegar apenas um usuario pelo ID"""


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=PublicClient
)
def read_cliente(user_id: int, session: Session = Depends(get_session)):

    cliente = session.scalar(
        select(Cliente).where(Cliente.idcliente == user_id)
    )

    if not cliente:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Id não encontrado nós Cliente',
        )

    return cliente


""" Rota para atualizar informações de um usuario pelo ID"""


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=PublicClient
)
def update_cliente(
    user_id: int,
    cliente: ClienteSchema,
    session: Session = Depends(get_session),
):

    db_user = session.get(Cliente, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
    db_user.email = cliente.email
    db_user.nome = cliente.nome
    db_user.cpf = cliente.cpf
    db_user.senha = cliente.senha

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


""" Rota para deletar um usuario informado o ID no path do URL"""


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=PublicClient
)
def delete_cliente(user_id: int, session: Session = Depends(get_session)):

    db_user = session.get(Cliente, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuáro que vai ser deletado não foi encontrado',
        )

    session.delete(db_user)
    session.commit()

    return db_user


@app.get('/lojas/', status_code=HTTPStatus.OK, response_model=LojasList)
def read_lojas(session: Session = Depends(get_session)):
    lojas = session.scalars(select(Lojas)).all()

    return {'lojas': lojas}


@app.get(
    '/lojas/{user_id}', status_code=HTTPStatus.OK, response_model=PublicLojas
)
def read_loja(user_id: int, session: Session = Depends(get_session)):

    db_loja = session.get(Lojas, user_id)

    if db_loja is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Id da loja não encontrado!',
        )

    return db_loja


@app.post(
    '/lojas/', status_code=HTTPStatus.CREATED, response_model=LojasSchema
)
def create_loja(loja: LojasSchema, session: Session = Depends(get_session)):
    db_loja = session.scalar(
        select(Lojas).where(
            (Lojas.email == loja.email) | (Lojas.cnpj == loja.cnpj)
        )
    )

    if db_loja:
        if loja.email == db_loja.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='email da loja já cadastrado!',
            )
        else:  
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='cnpj da loja já cadastrado!',
            )

    new_loja = Lojas(
        nome=loja.nome,
        email=loja.email,
        qtsvendas=loja.qtsvendas,
        ganhoVendas=loja.ganhoVendas,
        cnpj=loja.cnpj,
    )

    session.add(new_loja)
    session.commit()
    session.refresh(new_loja)

    return new_loja


@app.put(
    '/lojas/{user_id}',
    status_code=HTTPStatus.CREATED,
    response_model=PublicLojas,
)
def update_loja(
    user_id: int, loja: LojasSchema, session: Session = Depends(get_session)
):

    db_loja = session.get(Lojas, user_id)

    if db_loja is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Loja não não encontrada, para ser atualizada!',
        )

    db_loja.nome = loja.nome
    db_loja.email = loja.email
    db_loja.qtsvendas = loja.qtsvendas
    db_loja.ganhoVendas = loja.ganhoVendas
    db_loja.cnpj = loja.cnpj

    session.add(db_loja)
    session.commit()
    session.refresh(db_loja)

    return db_loja


@app.delete('/lojas/{loja_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_loja(loja_id: int, session: Session = Depends(get_session)):
    db_loja = session.get(Lojas, loja_id)

    if not db_loja:
        raise HTTPException(status_code=404, detail='Loja não encontrada')

    session.delete(db_loja)
    session.commit()


@app.get('/produtos/', status_code=HTTPStatus.OK)
def read_produtos(session: Session = Depends(get_session)):
    produtos = session.scalars(select(Produto)).all()
    return {'produtos': produtos}


@app.post('/produtos/', status_code=HTTPStatus.CREATED)
def create_produto(
    produto: ProdutoSchema, session: Session = Depends(get_session)
):

    db_produto = Produto(nome=produto.nome, preco=produto.preco)

    session.add(db_produto)
    session.commit()
    session.refresh(db_produto)

    return db_produto


@app.put(
    '/produtos/{user_id}',
    status_code=HTTPStatus.CREATED,
    response_model=ProdutoSchema,
)
def update_produto(
    user_id: int,
    produto: ProdutoSchema,
    session: Session = Depends(get_session),
):

    db_produto = session.get(Produto, user_id)

    if db_produto is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Produto não encontrado'
        )

    db_produto.nome = produto.nome
    db_produto.preco = produto.preco

    session.add(db_produto)
    session.commit()
    session.refresh(db_produto)


@app.delete('/produtos/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_produto(user_id: int, session: Session = Depends(get_session)):
    produto_db = session.scalar(
        select(Produto).where(Produto.idProduto == user_id)
    )

    if not produto_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Produto não encontrado'
        )

    session.execute(delete(Estoque).where(Estoque.id_produto == user_id))

    session.delete(produto_db)

    session.commit()


@app.get('/estoques/', status_code=HTTPStatus.OK)
def read_estoques(session: Session = Depends(get_session)):
    estoques = session.scalars(select(Estoque)).all()

    return {'estoques': estoques}


@app.get('/estoques/{produto_id}', status_code=HTTPStatus.OK)
def read_estoque(
        produto_id: int,
        session: Session = Depends(get_session)
        ):
    estoque = session.scalar(
        select(Estoque).where(
            Estoque.id_produto == produto_id
            )
    )
    if not estoque:
        raise HTTPException(
                status_code=404,
                detail='Estoque não encontrado'
                )
    return estoque


@app.post(
        '/estoques/',
        status_code=HTTPStatus.OK,
        response_model=EstoquePublic
        )
def create_estoque(
        estoque: EstoquePublic,
        session: Session = Depends(get_session)
        ):

    produto_db = session.scalar(
            select(Produto).where(
                Produto.idProduto == estoque.id_produto
                )
            )

    if produto_db is None:
        raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Id do produto não existe!"
                )

    estoque_exis = session.scalar(
            select(Estoque).where(
                Estoque.id_produto == produto_db.idProduto
                )
            )

    if estoque_exis:
        raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Estoque já existe!"
                )

    new_estoque = Estoque(
            id_produto=produto_db.idProduto,
            disponivel=estoque.disponivel
            )

    session.add(new_estoque)
    session.commit()
    session.refresh(new_estoque)

    return new_estoque


@app.put(
        '/estoque/{produto_id}',
        status_code=HTTPStatus.OK,
        response_model=EstoquePublic
        )
def update_estoque(
    produto_id: int,
    estoque_data: EstoquePublic,
    session: Session = Depends(get_session)
):
    db_estoque = session.scalar(
        select(Estoque).where(Estoque.id_produto == produto_id)
    )

    if not db_estoque:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Estoque para este produto não encontrado"
        )

    db_estoque.disponivel = estoque_data.disponivel

    session.add(db_estoque)
    session.commit()
    session.refresh(db_estoque)

    return db_estoque


@app.delete(
        '/estoque/{produto_id}',
        status_code=HTTPStatus.NO_CONTENT
        )
def delete_estoque(
        produto_id: int,
        session: Session = Depends(get_session)
        ):
    db_estoque = session.scalar(
        select(Estoque).where(Estoque.id_produto == produto_id)
    )

    if not db_estoque:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Registro de estoque não encontrado para este produto"
        )

    session.delete(db_estoque)

    session.commit()
