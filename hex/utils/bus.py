import aioamqp
import json


class Bus:
    def __init__(self) -> None:
        self.protocol = None
        self.channel = None

    @staticmethod
    async def make():
        bus = Bus()
        await bus.connect()

        return bus

    async def connect(self):
        _, protocol = await aioamqp.connect(host='0.0.0.0', port=5672, login='local', password='password')

        self.protocol = protocol
        self.channel = await self.protocol.channel()

    async def assert_queue(self, queue_name):
        await self.channel.queue(queue_name=queue_name, durable=True)

    async def bind_queue(self, queue_name, bindings):
        for binding in bindings:
            await self.channel.queue_bind(
                exchange_name=binding.get('context'),
                queue_name=queue_name,
                routing_key=binding.get('type')
            )

    async def create_handler(self, handler):
        async def handle_incoming_message(channel, body, envelope, properties):
            async def ack():
                await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)

            result = await handler(data=json.loads(body), ack=ack)

            return result

        return handle_incoming_message

    async def subscribe(self, handler, queue_name):

        new_handler = await self.create_handler(handler=handler)

        await self.channel.basic_qos(prefetch_count=1, prefetch_size=0, connection_global=False)
        await self.channel.basic_consume(new_handler, queue_name=queue_name)
