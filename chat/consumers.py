import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, User, Message
import requests


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connect to chat room."""
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Disconnect from chat room."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Receive message from WebSocket and send to room."""
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = text_data_json["user"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "user": user},
        )

    async def chat_message(self, event):
        """Receive message from room and send to WebSocket."""
        message = event["message"]
        user = event["user"]
        api_key = "AIzaSyBn2iHm0d7QM853HRKGvSX-IbvXGXeZmWw"
        url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
            + "?key="
            + api_key
        )
        data_dict = {
            "comment": {"text": message},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
            },
        }
        response = requests.post(url=url, data=json.dumps(data_dict))
        response_dict = json.loads(response.content)
        try:
            toxicity = response_dict["attributeScores"]["TOXICITY"]["summaryScore"][
                "value"
            ]
        except KeyError:
            print(response.status_code)
        await self.send(
            text_data=json.dumps(
                {"message": message, "user": user, "toxicity": toxicity}
            )
        )
