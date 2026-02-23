from dataclasses import asdict

from sqlalchemy import select

from loja_db.models import Cliente

""" Teste para ciração de usuarios no banco de dados"""


def test_create_user(session):
    new_user = Cliente(
        nome='test',
        email='test@example.com',
        senha='passwd',
        cpf='1234560',
    )

    session.add(new_user)
    session.commit()

    """ SELECT * FROM Client WHERE nome = test"""
    user = session.scalar(select(Cliente).where(Cliente.nome == 'test'))

    assert asdict(user) == {
        'id': 1,
        'nome': 'test',
        'email': 'test@example.com',
        'senha': 'passwd',
        'cpf': '1234560',
    }
