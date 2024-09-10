import requests


class APIClient:
    BASE_URL = 'http://127.0.0.1:8000'

    def register(self, data):
        url = f'{self.BASE_URL}/register'
        response = requests.post(url, data=data)
        return response

    def login(self, data):
        url = f'{self.BASE_URL}/login'
        response = requests.post(url, data=data)
        return response

    def get_user_profile(self, token):
        url = f'{self.BASE_URL}/user-profile'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        return response

    def edit_user_profile(self, token, data):
        url = f'{self.BASE_URL}/edit-profile'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.put(url, data=data, headers=headers)
        return response

    def change_password(self, token, data):
        url = f'{self.BASE_URL}/change-password'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(url, data=data, headers=headers)
        return response

    def reset_password(self, data):
        url = f'{self.BASE_URL}/reset-password'
        response = requests.post(url, data=data)
        return response

    def verify_code(self, data):
        url = f'{self.BASE_URL}/verify-code'
        response = requests.post(url, data=data)
        return response
