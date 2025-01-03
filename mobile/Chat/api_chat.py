import requests


class APIChat:
    BASE_URL = 'http://127.0.0.1:8000'

    def chat_room(self, token):
        url = f'{self.BASE_URL}/chat-room'
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        return response

    def chat_message(self, token, chat_id):
        url = f'{self.BASE_URL}/chat-message/{chat_id}/'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        return response

    def delete_chat(self, token, chat_id):
        url = f'{self.BASE_URL}/delete-chat/{chat_id}/'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.delete(url, headers=headers)
        return response

    def edit_chat_name(self, token, chat_id, data):
        url = f'{self.BASE_URL}/edit-chat-name/{chat_id}/'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.put(url, headers=headers, data=data)
        return response

    def block_user(self, token, data):
        url = f'{self.BASE_URL}/block-user'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(url, headers=headers, data=data)
        return response

    def create_chat(self, token, data):
        url = f'{self.BASE_URL}/create-chat'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=data)
        return response
