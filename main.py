import flet as ft
from googlesearch import search

def main(page: ft.Page):
    page.bgcolor="white"

    def openpage(e):
        wv = ft.WebView(
            url="https://flet.dev",
            on_page_started=lambda _: print("Page started"),
            on_page_ended=lambda _: print("Page ended"),
            on_web_resource_error=lambda e: print("Page error:", e.data),
            expand=True,
        )
        page.add(wv)
        page.update()
        

    def submission(e):
        query=searchbar.value
        links = [result for result in search(query, num_results=5)]
        for result in links:
            page.add(ft.TextButton(result, on_click=page.add(ft.WebView(
                                                                url=result,
                                                                on_page_started=lambda _: print("Page started"),
                                                                on_page_ended=lambda _: print("Page ended"),
                                                                on_web_resource_error=lambda e: print("Page error:", e.data),
                                                                expand=True,
                                                            ))))
        page.update()

    searchbar=ft.CupertinoTextField(placeholder_text="search...", placeholder_style=ft.TextStyle(color=ft.Colors.GREY_500), bgcolor=ft.Colors.GREY_300, color="black", on_submit=submission)
    wv = ft.WebView(
        url="https://flet.dev",
        on_page_started=lambda _: print("Page started"),
        on_page_ended=lambda _: print("Page ended"),
        on_web_resource_error=lambda e: print("Page error:", e.data),
        expand=True,
    )
    page.add(searchbar)

ft.app(main)