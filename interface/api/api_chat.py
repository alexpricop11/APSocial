import requests


class APIChat:
    BASE_URL = 'http://127.0.0.1:8000'

    def chat_room(self, token):
        url = f'{self.BASE_URL}/chat-room'
        headers = {'Authorization': f'Bearer {token}'}
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
