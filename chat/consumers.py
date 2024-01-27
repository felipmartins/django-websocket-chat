import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Chat, Visitor


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_uuid = self.scope["url_route"]["kwargs"]["room_uuid"]
        self.room_group_name = f"chat_{self.room_uuid}"

        visitor = Visitor.objects.get(id=self.scope["session"]["visitor_id"])
        chat = Chat.objects.get(uuid=self.room_uuid)

        if visitor not in chat.visitors.all():
            chat.add_visitor(visitor)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        visitor = Visitor.objects.get(id=self.scope["session"]["visitor_id"])
        chat = Chat.objects.get(uuid=self.room_uuid)

        chat.remove_visitor(visitor)

        chat.excludes_if_must()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        Chat.objects.get(uuid=self.room_uuid).add_message(message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({"message": message}))
