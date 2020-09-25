from datetime import datetime
from unittest.mock import Mock

import inject
import pytest

from hex.use_cases.search_posts import SearchPostsUseCase
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
    def test_search_posts(self, injector: None, database: Mock, post: Post) -> None:
        database.search_posts.return_value = [post]
        database.count_posts.return_value = 100

        result = SearchPostsUseCase().execute(start_after=10, end_before=90)

        assert result == ([post], 100)
        database.search_posts.assert_called_once_with(start_after=10, end_before=90)
        database.count_posts.assert_called_once_with()
