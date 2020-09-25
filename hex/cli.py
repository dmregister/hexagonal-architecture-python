import subprocess
from typing import Union

import click
import os
from dotenv import load_dotenv
from sqlalchemy import (create_engine)


def validate_env(_context: click.Context, _parameter: Union[click.Option, click.Parameter],
                 env: str) -> str:
    values = ('dev', 'test')
    if env not in values:
        raise click.BadParameter(f'`env` must be one of: {values}')

    return env


def database_exists(engine, database):
    result_proxy = engine.execute("SELECT 1 FROM pg_database WHERE datname='%s'" % database)
    result = result_proxy.scalar()
    result_proxy.close()
    engine.dispose()
    return result


def load_env(env):
    dotenv_file = '.env'
    if env != 'dev':
        dotenv_file = f'.env.{env}'

    load_dotenv(dotenv_file, override=True)


@click.group('Hex server CLI')
def cli() -> None:
    pass


@cli.command(help='Run the use_cases server')
@click.argument('env', envvar='ENV', default='dev', callback=validate_env)
def server(env: str) -> int:
    load_env(env)
    return subprocess.call(['flask', 'run'])


@cli.group(help="Manage the database")
def db() -> None:
    pass


@db.command(help="Create the database")
@click.argument('env', envvar='ENV', default='dev', callback=validate_env)
def create(env: str) -> int:
    load_env(env)
    click.echo(f'Creating database for `{env}` environment...')

    db_name = f'hex_{env}'

    engine = create_engine(os.getenv('DATABASE_URI'))

    if database_exists(engine, db_name):
        print(f'{db_name} database already exist')
        return 1

    conn = engine.connect()
    conn.execute("COMMIT")
    conn.execute(f'CREATE DATABASE {db_name}')
    conn.close()

    return 1


@db.command(help="Run the database migrations")
@click.argument('env', envvar='ENV', default='dev', callback=validate_env)
def migrate(env: str) -> int:
    load_env(env)
    click.echo(f'Running migrations for `{env}` environment...')

    return subprocess.call(['alembic', 'upgrade', 'head'])


@cli.group(help='Run the code quality tools')
def check() -> None:
    pass


@check.command(help='Run the linter')
def style() -> int:
    click.echo('Running `flake8`...')
    return subprocess.call('flake8')


@check.command(help='Run the test suite')
def tests() -> int:
    load_env('test')
    click.echo('Running `pytest`...')
    return subprocess.call('pytest')


@check.command(help='Run the static analyzer')
def types() -> int:
    click.echo('Running `mypy`...')
    return subprocess.call('mypy')
