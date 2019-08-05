"""Invoke tasks.py

Details see manual: http://docs.pyinvoke.org/en/1.0/getting-started.html
"""
from invoke import task


SRC_DIR = 'app/'


@task
def install(ctx):
    """Install dependencies."""
    ctx.run('pipenv install')


@task
def test(ctx):
    """Install dependencies."""
    ctx.run('py.test')


@task
def serve(ctx, pip=False):
    if pip:
        install(ctx)
    print('Serving server ')


@task
def yapf(ctx):
    """Run yapf."""
    ctx.run(f'yapf -i --recursive  {SRC_DIR}')


@task
def flake8(ctx):
    """Run flake8."""
    ctx.run(f'flake8 {SRC_DIR}')


@task
def isort(ctx):
    """Run isort."""
    ctx.run(f'isort -rc {SRC_DIR}')


@task(pre=[isort, yapf, flake8])
def lint(ctx):
    """Run linters."""
