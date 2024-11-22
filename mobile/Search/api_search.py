import requests


class APISearchUser:
    BASE_URL = 'http://127.0.0.1:8000'

    def search_user(self, token, user):
        url = f'{self.BASE_URL}/search-user/{user}/'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        return response

    def get_history_search(self, token):
        url = f'{self.BASE_URL}/history-search'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        return response

    def save_user_history(self, token, searched_username):
        url = f'{self.BASE_URL}/save-user'
        headers = {'Authorization': f'Bearer {token}'}
        data = {'searched_username': searched_username}
        response = requests.post(url, headers=headers, data=data)
        return response

    def delete_user_from_history(self, token, user):
        url = f'{self.BASE_URL}/delete-user'
        headers = {'Authorization': f'Bearer {token}'}
        data = {'searched_user': user}
        response = requests.delete(url, headers=headers, json=data)
        return response
