import requests


class APISearchUser:
    BASE_URL = 'http://127.0.0.1:8000'

    def search_user(self, token, user):
        url = f'{self.BASE_URL}/search-user/{user}/'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        return response
