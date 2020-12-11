import os

import inject
from flask import Flask

from hex.adapters.outgoing.persistence.post_repository import PostRepository
from hex.adapters.outgoing.persistence.database_interface import DatabaseInterface


def configure_application(application: Flask) -> None:
    application.config.update(
        DATABASE_URI=f"{os.getenv('DATABASE_URI')}/hex_{os.getenv('ENV')}"
    )


def configure_inject(application: Flask) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(DatabaseInterface, PostRepository(application.config['DATABASE_URI']))
        # binder.bind(RabbitMqClient, PostRepository(application.config['DATABASE_URI']))

    inject.configure(config)
