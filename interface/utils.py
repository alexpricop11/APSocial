from api.api_client import APIClient


def get_user_status(page, response, token):
    if page.route == '/home':
        data = {'user_id': response.json().get('id'), 'online': True}
    else:
        data = {'user_id': response.json().get('id'), 'online': False}
    APIClient().user_status(token, data)


def get_theme_mode(page):
    saved_theme = page.client_storage.get("theme_mode")
    if saved_theme is None:
        saved_theme = "dark"
    page.theme_mode = saved_theme


def get_token(page):
    token = page.client_storage.get("token")
    if token:
        response = APIClient().get_user_profile(token)
        if response.status_code == 200:
            page.go('/home')
            get_user_status(page, response, token)
        else:
            page.go('/auth')
            get_user_status(page, response, token)
    else:
        page.go('/auth')
