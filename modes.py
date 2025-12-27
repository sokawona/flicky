# import flet as ft



# def open_modes_dialog(page: ft.Page, db, state, next_callback):
#     all_tags = db.get_all_tags()

#     def toggle_reverse(e):
#         state['reverse_mode'] = e.control.value
#         db.set_setting('reverse_mode', str(e.control.value))
#         next_callback(None) 

#     def toggle_flexible(e):
#         state['flexible_mode'] = e.control.value
#         db.set_setting('flexible_mode', str(e.control.value))
#         tags_container.visible = e.control.value
#         page.update()

#     def on_tag_change(e, tag):
#         if e.control.value:
#             if tag not in state['selected_tags']:
#                 state['selected_tags'].append(tag)
#         else:
#             if tag in state['selected_tags']:
#                 state['selected_tags'].remove(tag)
        
#         db.set_setting('selected_tags', ",".join(state['selected_tags']))

#     tag_checkboxes = [
#         ft.Checkbox(
#             label=tag, 
#             value=tag in state['selected_tags'],
#             on_change=lambda e, t=tag: on_tag_change(e, t)
#         ) for tag in all_tags
#     ]

#     tags_container = ft.Column(
#         controls=[
#             ft.Text("Choose tags:", size=14, weight="bold"),
#             *tag_checkboxes
#         ],
#         visible=state['flexible_mode'],
#         scroll=ft.ScrollMode.ADAPTIVE,
#         tight=True
#     )

#     dialog = ft.AlertDialog(
#         title=ft.Text("Mode settings"),
#         content=ft.Container(
#             content=ft.Column([
#                 ft.Switch(
#                     label="Reverse (Translate -> Word)", 
#                     value=state['reverse_mode'], 
#                     on_change=toggle_reverse
#                 ),
#                 ft.Switch(
#                     label="Flexible (Tags filter)", 
#                     value=state['flexible_mode'], 
#                     on_change=toggle_flexible
#                 ),
#                 ft.Divider(),
#                 tags_container
#             ], tight=True, width=300),
#         ),
#         actions=[
#             ft.FilledButton("OK", on_click=lambda _: (setattr(dialog, "open", False), page.update()))
#         ]
#     )

#     page.overlay.append(dialog)
#     dialog.open = True
#     page.update()

import flet as ft

def open_modes_dialog(page: ft.Page, db, sm, state, next_callback):

    all_tags = db.get_all_tags()

    def toggle_reverse(e):
        state['reverse_mode'] = e.control.value
        # Сохраняем через менеджер
        sm.save_mode('reverse_mode', e.control.value)
        next_callback(None) 

    def toggle_flexible(e):
        state['flexible_mode'] = e.control.value
        sm.save_mode('flexible_mode', e.control.value)
        tags_container.visible = e.control.value
        page.update()

    def on_tag_change(e, tag):
        if e.control.value:
            if tag not in state['selected_tags']:
                state['selected_tags'].append(tag)
        else:
            if tag in state['selected_tags']:
                state['selected_tags'].remove(tag)
        
        sm.save_tags(state['selected_tags'])

    # Создаем чекбоксы
    tag_checkboxes = [
        ft.Checkbox(
            label=tag, 
            value=tag in state['selected_tags'],
            on_change=lambda e, t=tag: on_tag_change(e, t)
        ) for tag in all_tags
    ]

    tags_container = ft.Column(
        controls=[
            ft.Text("Choose tags:", size=14, weight="bold"),
            ft.Container(
                content=ft.Column(
                    tag_checkboxes, 
                    spacing=0, 
                    scroll=ft.ScrollMode.AUTO),
                height=200,
            )
        ],
        visible=state['flexible_mode'],
        tight=True
    )

    dialog = ft.AlertDialog(
        title=ft.Text("Mode settings"),
        content=ft.Container(
            content=ft.Column([
                ft.Switch(
                    label="Reverse (Translate -> Word)", 
                    value=state['reverse_mode'], 
                    on_change=toggle_reverse
                ),
                ft.Switch(
                    label="Flexible (Tags filter)", 
                    value=state['flexible_mode'], 
                    on_change=toggle_flexible
                ),
                ft.Divider(),
                tags_container
            ], tight=True, width=300),
        ),
        actions=[
            ft.FilledButton("Done", on_click=lambda _: (setattr(dialog, "open", False), page.update()))
        ]
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()
