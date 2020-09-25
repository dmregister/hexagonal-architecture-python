import inject

from hex.domain.post import Post
from hex.adapters.outgoing.persistence.database_interface import DatabaseInterface


class GetPostUseCase:
    @inject.autoparams()
    def __init__(self, database: DatabaseInterface):
        self.__database = database

    def execute(self, post_id: int) -> Post:
        return self.__database.get_post(post_id)
