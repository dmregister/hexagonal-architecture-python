from datetime import datetime
from unittest.mock import Mock

import inject
import pytest

from hex.use_cases.get_posts import GetPostUseCase
from hex.domain.post import Post
from hex.adapters.outgoing.persistence.database_interface import DatabaseInterface


@pytest.fixture
def database() -> Mock:
    return Mock()


@pytest.fixture
def injector(database: Mock) -> None:
    inject.clear_and_configure(lambda binder: binder
                               .bind(DatabaseInterface, database))


@pytest.fixture
def post() -> Post:
    return Post(id=1,
                author_name='Alex',
                title='Test Post',
                body='A longer body for this post',
                created_at=datetime.now(),
                updated_at=datetime.now())


class TestPosts:
    def test_get_posts(self, injector: None, database: Mock, post: Post) -> None:
        database.get_post.return_value = post

        result = GetPostUseCase().execute(1)

        assert result == post
        database.get_post.assert_called_once_with(1)
