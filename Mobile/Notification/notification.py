import flet as ft


class Notification(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return ft.SafeArea(ft.Text("Notificare"))
