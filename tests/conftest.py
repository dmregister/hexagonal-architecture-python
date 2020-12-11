import os
from typing import Optional

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

from hex.adapters.outgoing.persistence.post_repository import metadata


@pytest.fixture
def database_uri() -> Optional[str]:
    return f"{os.getenv('DATABASE_URI')}/hex_{os.getenv('ENV')}"


@pytest.fixture
def database_connection(database_uri: str) -> Connection:
    engine = create_engine(database_uri)
    connection = engine.connect()
    for table in metadata.sorted_tables:
        connection.execute(table.delete())
    return connection
