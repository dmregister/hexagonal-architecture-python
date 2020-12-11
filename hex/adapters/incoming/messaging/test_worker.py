import hex.use_cases.get_posts as GetPostUseCase


app_name = 'test'
context = 'test'
name = 'test-queue'

bindings = [
    {'type': 'foo', 'context': 'bar'},
    {'type': 'bar', 'context': 'foo'}
]

validate = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": f"{name} validation",
  "type": "object",
  "properties": {
    "customerId": {
      "type": "string",
      "description": "The id of the customer"
    }
  }
}


def setup(container):

    use_case = container.instance(GetPostUseCase)

    async def handle(data) -> None:
        post_id = 2

        print(" [x] Received %r in test_worker" % data)

        try:
            post = use_case.execute(post_id=post_id)
            print(f" post found with id: {post_id}")
        except ValueError:
            print(f" no post found with id: {post_id}")

        print(" [x] Done")

    return handle
