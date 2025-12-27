import asyncio
import flet as ft
import time 
from dict import show_words_list
from database import Database   
from modes import open_modes_dialog
from settings_manager import SettingsManager


def main(page: ft.Page):
    page.title = 'flicky'
    page.fonts = {
        "JB Mono": "JetBrainsMono.ttf",
    }
    page.theme = ft.Theme(
        font_family="JB Mono",
        visual_density=ft.VisualDensity.COMFORTABLE,
    )

    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    db = Database()
    sm = SettingsManager(db)

    saved_reverse = db.get_setting("reverse_mode", "False") == "True"
    saved_flex = db.get_setting("flexible_mode", "False") == "True"
    saved_tags_str = db.get_setting("selected_tags", "")
    saved_tags = saved_tags_str.split(",") if saved_tags_str else []

    saved_theme = db.get_setting("theme_mode", "light") 
    if saved_theme == "dark":
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT

    state = {
        'current_word': db.get_random(),
        'is_flipped': False,
        'last_flip_time': 0,
        'reverse_mode': saved_reverse,
        'flexible_mode': saved_flex,
        'selected_tags': saved_tags,
        'last_tag': sm.load_last_tag()
    }

    word_text = ft.Text(
        value=state['current_word']['main'] if state['current_word'] else "Add words",
        size=25, 
        color=ft.Colors.BLACK,
        font_family="JB Mono",
        text_align=ft.TextAlign.CENTER
    )


    card_content = ft.Container(
        content=word_text,
        width=300,
        height=450,
        border_radius=20,
        alignment=ft.Alignment(0, 0),
        bgcolor=ft.Colors.WHITE, 
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, "black")),
        padding=20,
        border=ft.Border.all(width=1, color=ft.Colors.BLACK),
        opacity=1, 
        animate_opacity=ft.Animation(300, ft.AnimationCurve.DECELERATE)
        
    )

    card = ft.GestureDetector(
        content=card_content,
        on_tap=lambda _: flip(),             
    )

    f_main = ft.TextField(label= 'Word')
    f_trans = ft.TextField(label= 'Transcription')
    f_tranl = ft.TextField(label= 'Translate')
    f_tag = ft.TextField(label='Tag', value=state['last_tag'])




    def refresh_main_screen():
        next()

    def flip():
        if state['current_word'] is None:
            return

        current_time = time.time()
        if current_time - state['last_flip_time'] < 0.3:
            return

        state['last_flip_time'] = current_time
        state['is_flipped'] = not state['is_flipped']

        if state['is_flipped']:
            if not state['reverse_mode']: #! reverse OFF
                word_text.value = f"{state['current_word']['transcription']}\n{state['current_word']['translate']}"
            else:   #! reverse ON
                word_text.value = f"{state['current_word']['main']}\n{state['current_word']['transcription']}"
        else:
            if not state['reverse_mode']: #! reverse OFF
                word_text.value = state['current_word']['main']
            else:   #! reverse ON
                word_text.value = state['current_word']['translate']
            
        page.update()

    def next(e=None):
        new_word = db.get_random(active_tags=state['selected_tags'] if state['flexible_mode'] else None)
        
        if new_word:
            state['current_word'] = new_word
            state['is_flipped'] = False

            if state['reverse_mode']:
                word_text.value = state['current_word']['translate'] 
            else:
                word_text.value = state['current_word']['main'] 
                word_text.size = 25
        else:
            state['current_word'] = None
            word_text.value = "Add words"
            word_text.size = 25
            
        page.update()


    def save_word(e):
        if f_main.value:
            db.add_word(
                f_main.value,
                f_trans.value, 
                f_tranl.value, 
                f_tag.value
                )
            state['last_tag'] = f_tag.value
            sm.save_last_tag(f_tag.value)

            f_main.value = f_trans.value = f_tranl.value = ""
            f_tag.value = 'default'
            add_dialog.open = False
            next() 
            page.update()

    add_dialog = ft.AlertDialog(
        title=ft.Text('Add word'),
        content=ft.Column([f_main, f_trans, f_tranl, f_tag], tight=True),
        actions=[
            ft.TextButton('Cancel', on_click=lambda _: (setattr(add_dialog, "open", False), page.update())),
            ft.FilledButton('Save', on_click= save_word)
        ]
    )
    page.overlay.append(add_dialog)


    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.DARK_MODE
            card.bgcolor = ft.Colors.WHITE
            word_text.color = ft.Colors.BLACK
            db.set_setting("theme_mode", "light") 
        else:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.LIGHT_MODE
            card.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST
            word_text.color = ft.Colors.BLACK
            db.set_setting("theme_mode", "dark") 
        page.update()

    def open_info_dialog(e):
        page = e.page  # Получаем объект страницы

        # В 2025 году метод называется launch_url
        async def launch_link(url):
            await page.launch_url(url)

        info_dialog = ft.AlertDialog(
            title=ft.Text("Info"),
            content=ft.Column([
                ft.Text("Следить за обновлениями:", weight="bold", size=14),
                
                # ИСПРАВЛЕНО: добавлен протокол https://
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.TELEGRAM, color=ft.Colors.BLUE_400),
                    title=ft.Text("Telegram", color=ft.Colors.BLUE_400),
                    on_click=lambda _: page.run_task(launch_link, "https://t.me/flickyapp"),
                ),
                
                # ИСПРАВЛЕНО: чистая ссылка на репозиторий
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.CODE, color=ft.Colors.GREY_900),
                    title=ft.Text("GitHub Repo", color=ft.Colors.GREY_900),
                    on_click=lambda _: page.run_task(launch_link, "https://github.com/sokawona/Flicky.git"),
                ),
            ], tight=True, spacing=5),
            actions=[
                ft.TextButton("Закрыть", on_click=lambda _: (setattr(info_dialog, "open", False), page.update()))
            ]
        )

        page.overlay.append(info_dialog)
        info_dialog.open = True
        page.update()





    theme_button = ft.IconButton( icon=ft.Icons.LIGHT_MODE,icon_color=ft.Colors.BLACK, on_click=toggle_theme)

    theme_container = ft.Container(
        content=theme_button,
        padding=10,
    )   


    bottom_buttons = ft.Container(
        content=ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.MENU, 
                    icon_color=ft.Colors.BLACK,
                    on_click=lambda _: show_words_list(page, db, sm, refresh_main_screen)
                ),
                ft.IconButton(
                    icon=ft.Icons.ADD, 
                    icon_color=ft.Colors.BLACK,
                    on_click=lambda _: (setattr(add_dialog, "open", True), page.update())
                ),
                ft.IconButton(
                    icon=ft.Icons.TUNE,
                    icon_color=ft.Colors.BLACK,
                    on_click=lambda _: open_modes_dialog(page, db, sm, state, next)
                ),
                theme_button,
                ft.IconButton(
                    icon=ft.Icons.INFO_OUTLINE, 
                    icon_color=ft.Colors.BLACK,
                    tooltip="Help & Info",
                    on_click=open_info_dialog
                ),
            ],
            tight=True,
        ),
        padding=5,
        bgcolor=ft.Colors.WHITE, 
        border_radius=15, 
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, "black")),
        border=ft.Border.all(width=1, color=ft.Colors.BLACK),
    )

    central_content = ft.Column(
        [
            card,
            ft.Row(
                [
                    ft.FilledButton(
                        content=ft.Text(
                        "->", 
                        size=22,          
                        weight="bold"),
                        on_click=next,
                        width=100,  
                        height=60,  
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20 
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )


    page.add(
        ft.Stack([
            ft.Container(
                content=central_content, 
                top=150,
                left=0, 
                right=0
            ),  
            ft.Container(
                bottom_buttons,
                right=0,
                left=0,
                bottom=60,
                alignment=ft.Alignment(0, 1)
            ),
        ], expand=True)
    )



ft.run(main)