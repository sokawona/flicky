import flet as ft




def show_words_list(page: ft.Page, db, sm, on_change_callback):
    
    def open_edit_dialog(word_id, main, trans, transl, tag):
        # Поля ввода, предзаполненные текущими данными
        edit_main = ft.TextField(label="Word", value=main)
        edit_trans = ft.TextField(label="Transcription", value=trans)
        edit_transl = ft.TextField(label="Translate", value=transl)
        edit_tag = ft.TextField(label="Tag", value=tag)

        def save_changes(e):
            # Метод update должен быть в твоем database.py
            db.update_word(word_id, edit_main.value, edit_trans.value, edit_transl.value, edit_tag.value)
            sm.save_last_tag(edit_tag.value) 
            edit_dialog.open = False
            bs.open = False # Закрываем список для обновления
            page.update()
            on_change_callback() # Обновляем главную карточку
            show_words_list(page, db, sm, on_change_callback) # Переоткрываем список

        def delete_word(e):
            db.delete(word_id)
            edit_dialog.open = False
            bs.open = False
            page.update()
            on_change_callback()
            show_words_list(page, db, sm,  on_change_callback)

        edit_dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Text("Edit Word"),
                # Кнопка удаления в верхнем правом углу диалога
                ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color="red", on_click=delete_word)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            content=ft.Column([edit_main, edit_trans, edit_transl, edit_tag], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: (setattr(edit_dialog, "open", False), page.update())),
                ft.FilledButton("Save", on_click=save_changes)
            ]
        )

        page.overlay.append(edit_dialog)
        edit_dialog.open = True
        page.update()

    all_words = db.get_all() # Ожидаем: id, main, trans, transl, tag
    items = []
    
    for w in all_words:
        items.append(
            ft.ListTile(
                title=ft.Text(w[1]), 
                subtitle=ft.Text(f"{w[2]} — {w[3]} | {w[4]}"), # Добавили показ тега
                trailing=ft.IconButton(
                    ft.Icons.EDIT_OUTLINED, # Меняем иконку на карандаш
                    on_click=lambda _, word=w: open_edit_dialog(word[0], word[1], word[2], word[3], word[4])
                )
            )
        )

    if not items:
        items.append(ft.Container(ft.Text('List is empty'), padding=20))

    bs = ft.BottomSheet(
        ft.Container(
            ft.Column(items, scroll=ft.ScrollMode.ADAPTIVE, tight=True, height=page.height * 0.8),
            padding=10,
            bgcolor="surfaceVariant",
            border_radius=ft.border_radius.only(top_left=20, top_right=20)
        ),
        dismissible=True,
    )

    page.overlay.append(bs)
    bs.open = True
    page.update()


# import flet as ft



# def show_words_list(page: ft.Page, db, on_change_callback):
#     def delete_and_refresh(word_id):
#         db.delete(word_id)
#         bs.open = False
#         page.update()
#         show_words_list(page, db, on_change_callback)
#         on_change_callback() 

#     all_words = db.get_all()
    
#     items = []
#     for w in all_words:
#         items.append(
#             ft.ListTile(
#                 title=ft.Text(w[1]), 
#                 subtitle=ft.Text(f"{w[2]} — {w[3]}"), 
#                 trailing=ft.IconButton(
#                     ft.Icons.DELETE_OUTLINE, 
#                     icon_color=ft.Colors.RED_400,
#                     on_click=lambda _, w_id=w[0]: delete_and_refresh(w_id)
#                 )
#             )
#         )

#     if not items:
#         items.append(ft.Container(ft.Text('List is empty'), padding=20))


#     bs = ft.BottomSheet(
#         ft.Container(
#             ft.Column(items, scroll=ft.ScrollMode.ADAPTIVE, tight=True),
#             padding=10,
#             bgcolor="surfaceVariant", # Используем строковое название (CamelCase)
#             border_radius=ft.border_radius.only(top_left=20, top_right=20)
#         ),
#         dismissible=True,
#     )

#     page.overlay.append(bs)
#     bs.open = True
#     page.update()