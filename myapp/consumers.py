import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ActiveInactiveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            "active_users",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "active_users",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data,data['name'])
        # if data['status'] == 'active':
        #     # Handle active status
        #     await self.channel_layer.group_send(
        #         "active_users",
        #         {
        #             "type": "user_active",
        #             "status": 'active',
        #         }
        #     )
        # elif data['status'] == 'inactive':
        #     # Handle inactive status
        #     await self.channel_layer.group_send(
        #         "active_users",
        #         {
        #             "type": "user_inactive",
        #             "status": 'active',
        #         }
        #     )
        await self.channel_layer.group_send(
              "active_users",
                {
                    "type": "user_active",
                    "name": data['name'],
                    "message": data['message'],
                }


         )

    async def user_active(self, event):
        name = event['name']
        message = event['message']
        await self.send(text_data=json.dumps({
            'name': name,
            'message':message
        }))

    async def user_inactive(self, event):
        message = event['status']
        await self.send(text_data=json.dumps({
            'message': message
        }))
