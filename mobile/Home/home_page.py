import flet as ft


class HomePage(ft.UserControl):
    def __init__(self):
        super().__init__()

    @staticmethod
    def app_bar():
        app_bar = ft.Container(
            ft.Row(controls=[
                ft.Text("AP Social", expand=True, text_align=ft.TextAlign.CENTER, size=20, color=ft.colors.GREEN),
            ]
            ), padding=10, margin=-10
        )
        return app_bar

    def build(self):
        text = ft.Text('Acasă', size=25)
        appbar = ft.Container(ft.Column([
            self.app_bar(), text
        ]))
        return appbar
