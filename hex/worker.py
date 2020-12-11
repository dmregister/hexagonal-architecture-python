import asyncio
import inject
import os
from jsonschema import validate
import hex.use_cases.get_posts as GetPostUseCase
from hex.adapters.outgoing.persistence.post_repository import PostRepository
from hex.utils.bus import Bus
from hex.adapters.incoming.messaging import test_worker, test_worker_2


WORKERS_TO_REGISTER = [test_worker, test_worker_2]


class Worker:
    def __init__(self, bus: Bus) -> None:
        self.bus = bus

    @staticmethod
    def validate_message(data, handler):
        validate(instance=data, schema=handler.validate)

    async def handle_message(self, handler):
        async def process_message(data, ack):
            try:
                Worker.validate_message(data=data.get('data'), handler=handler)

                result = await handler.handle(data=data)

                await ack()

                return result
            except Exception as e:
                print(e)
                await ack()

        return process_message

    async def register_handler(self, handler):

        queue_name = f'{handler.app_name}.{handler.context}.{handler.name}'
        new_handler = await self.handle_message(handler=handler)

        await self.bus.assert_queue(queue_name=queue_name)
        await self.bus.bind_queue(queue_name=queue_name, bindings=handler.bindings)
        await self.bus.subscribe(handler=new_handler, queue_name=queue_name)


async def register_workers():
    bus = await Bus.make()
    worker = Worker(bus=bus)

    for handler in WORKERS_TO_REGISTER:
        composed_handler = handler.setup(inject.get_instance())
        await worker.register_handler(handler=composed_handler)


def config_application():
    def config(binder: inject.Binder) -> None:
        binder.bind(PostRepository, PostRepository(f"{os.getenv('DATABASE_URI')}/hex_{os.getenv('ENV')}"))
        binder.bind(GetPostUseCase, GetPostUseCase.setup())



    inject.configure(config, bind_in_runtime=False)




async def run():
    config_application()
    await register_workers()


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(run())
event_loop.run_forever()
