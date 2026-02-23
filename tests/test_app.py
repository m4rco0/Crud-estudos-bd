from http import HTTPStatus


def test_read_main(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'hello, world!'}


def test_create_cliente(client):
    response = client.post(
        '/users/',
        json={
            'nome': 'alice',
            'senha': 'passwd',
            'email': 'alice@example.com',
            'cpf': '123.321.444-02',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'nome': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_clientes(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'clientes': [
            {
                'email': 'alice@example.com',
                'nome': 'alice',
                'id': 1,
            },
        ],
    }


def test_read_cliente(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'alice@example.com',
        'nome': 'alice',
        'id': 1,
    }


def test_read_cliente_not_found(client):
    response = client.get('/user/-1')

    print(response.json())
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'Not Found',
    }


def test_update_cliente(client):
    response = client.put(
        '/users/1',
        json={
            'nome': 'bob',
            'email': 'bob@example.com',
            'cpf': '123456789',
            'senha': 'mynewpasswd',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'nome': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_cliente_not_found(client):
    response = client.put(
        '/users/-1',
        json={
            'nome': 'bob',
            'email': 'bob@example.com',
            'cpf': '123456789',
            'senha': 'mynewpasswd',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Não temos o user_id!'}


def test_delete_cliente(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'nome': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_cliente_not_found(client):
    response = client.delete('/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'User id para ser deletado, não existe!',
    }
