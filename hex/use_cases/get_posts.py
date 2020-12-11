import inject
from hex.domain.post import Post
from hex.adapters.outgoing.persistence.post_repository import PostRepository


def setup():
    post_repository = inject.instance(PostRepository)

    def execute(post_id: int) -> Post:
        return post_repository.get_post(post_id)

    return execute
