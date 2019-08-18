import pytest


@pytest.fixture(scope='session')
def session_id():
    from uuid import uuid4

    return str(uuid4())


@pytest.fixture(scope='session')
def unused_port():
    import socket

    def factory():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            return s.getsockname()[1]

    return factory


@pytest.fixture(scope='session')
def docker():
    import docker

    cli = docker.from_env()
    yield cli

    cli.close()
