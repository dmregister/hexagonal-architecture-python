import asyncio


app_name = 'test'
context = 'test'
name = 'test-queue-2'

bindings = [
    {'type': 'foo', 'context': 'bar'}
]

validate = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": f"{name} validation",
  "type": "object",
  "properties": {
    "customerId": {
      "type": "string",
      "description": "The person's first name."
    }
  }
}


async def handle(data) -> None:
    print(" [x] Received %r in test_worker_2" % data)
    await asyncio.sleep(len(data))
    print(" [x] Done")

