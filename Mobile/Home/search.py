import flet as ft
import sqlite3
import base64


class Search(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.result_list = ft.ListView()

    def search_bar(self):
        search = ft.SearchBar(
            view_elevation=10,
            divider_color=ft.colors.BLACK,
            bar_hint_text='Caută...',
            on_change=self.search_user,
            controls=[self.result_list]
        )
        return search

    def search_user(self, e):
        search_text = e.control.value.strip()
        if not search_text:
            self.result_list.controls.clear()
            self.update()
            return

        with sqlite3.connect('users.db') as db:
            cur = db.cursor()
            try:
                cur.execute("""SELECT profile_photo, username FROM users WHERE username LIKE ?""",
                            ('%' + search_text + '%',))
                result = cur.fetchall()
                self.result_list.controls.clear()
                if result:
                    for row in result:
                        profile_photo = row[0]
                        user = row[1]
                        if profile_photo:
                            user_image = ft.Image(src_base64=profile_photo, width=50, height=50, border_radius=50,
                                                  fit=ft.ImageFit.COVER)
                        else:
                            user_image = ft.Icon(name=ft.icons.PERSON, size=50, color=ft.colors.BLACK)
                        user_row = ft.Row([user_image, ft.Text(user)])
                        user_button = ft.Container(
                            content=user_row,
                            on_click=lambda e, username=user: self.on_user_click(username),
                            bgcolor=ft.colors.TRANSPARENT,
                            ink=True
                        )
                        self.result_list.controls.append(user_button)
                else:
                    self.result_list.controls.append(
                        ft.Text("Niciun rezultat găsit", color=ft.colors.RED)
                    )
            except sqlite3.Error as e:
                print(f"Eroare de bază de date: {e}")
                self.result_list.controls.append(
                    ft.Text("A apărut 0 eroare în timpul căutării", color=ft.colors.RED)
                )
        self.update()

    def on_user_click(self, username):
        print(f"Ai făcut clic pe utilizatorul: {username}")

    def build(self):
        return ft.SafeArea(ft.Column(
            [self.search_bar()]
        ))
