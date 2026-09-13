import flet as ft
import json, os

FILE = "mydata.json"
def load():
    if not os.path.exists(FILE): 
        return {"user": None, "posts": []}
    try:
        with open(FILE,"r",encoding="utf-8") as f: 
            return json.load(f)
    except: 
        return {"user": None, "posts": []}

def save(d):
    with open(FILE,"w",encoding="utf-8") as f: 
        json.dump(d,f,ensure_ascii=False)

def main(page: ft.Page):
    page.title = "Apna Gaon"
    page.bgcolor = "black"
    page.padding = 0

    def show_upload_page(t):
        page.clean()
        caption = ft.TextField(label="Caption likho...", width=320, bgcolor="white", color="black", border_radius=12, multiline=True)
        file_name = ft.TextField(label=f"{t} File Name", width=320, bgcolor="white", color="black", border_radius=12, value=f"my_{t.lower()}.mp4")
        def do_final_upload(e):
            d = load()
            d["posts"].append({"type": t, "file": file_name.value, "caption": caption.value})
            if d["user"]:
                d["user"]["posts_count"] = str(len(d["posts"]))
            save(d)
            show_profile()
        
        page.add(ft.Column([
            ft.Container(padding=15, content=ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda e: show_profile()),
                ft.Text(f"New {t}", color="white", size=18)
            ], spacing=10)),
            ft.Container(padding=15, content=ft.Column([
                caption, file_name, 
                ft.ElevatedButton(f"Upload {t}", on_click=do_final_upload, width=320, bgcolor="#d62976", color="white", height=50),
                ft.TextButton("Cancel", on_click=lambda e: show_profile())
            ]))
        ], scroll=ft.ScrollMode.AUTO, expand=True))

    def create_option(icon_name, text):
        return ft.Container(padding=18, on_click=lambda e: close_and_open(text), content=ft.Row([
            ft.Icon(icon_name, color="white", size=22), 
            ft.Text(text, color="white", size=16)
        ], spacing=15))

    def close_and_open(txt):
        sheet.open = False
        page.update()
        show_upload_page(txt)

    sheet = ft.BottomSheet(
        bgcolor="#121212", 
        content=ft.Column([
            ft.Container(padding=15, content=ft.Text("Create", color="white", size=20, weight="bold", text_align="center")),
            create_option(ft.Icons.VIDEO_LIBRARY, "Reel"),
            create_option(ft.Icons.GRID_ON, "Post"),
            create_option(ft.Icons.ADD_CIRCLE_OUTLINE, "Story")
        ], tight=True)
    )
    page.overlay.append(sheet)

    def open_create(e):
        sheet.open = True
        page.update()

    def show_profile():
        page.clean()
        d = load()
        u = d["user"]
        if not u:
            show_register()
            return
        col = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=[
            ft.Container(padding=15, content=ft.Row([
                ft.IconButton(icon=ft.Icons.ADD, icon_color="white", on_click=open_create),
                ft.Text(u.get("username",""), color="white", size=18, weight="bold", expand=True)
            ]))
        ])
        page.add(col)

    def show_register():
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        uname = ft.TextField(label="Username*", width=300, bgcolor="white", color="black", border_radius=15)
        pwd = ft.TextField(label="Password*", password=True, width=300, bgcolor="white", color="black", border_radius=15)
        def do_reg(e):
            if uname.value=="" or pwd.value=="":
                return
            save({"user": {"username": uname.value, "password": pwd.value, "name": uname.value, "line1": "", "line2": "", "link": "", "followers": "0", "following": "0", "posts_count": "0"}, "posts": []})
            show_profile()
        page.add(ft.Column([
            ft.Text("Apna Gaon", color="white", size=30, weight="bold"), 
            uname, pwd, 
            ft.ElevatedButton("Register", on_click=do_reg, width=300, bgcolor="#d62976", color="white")
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER))

    if not load()["user"]:
        show_register()
    else:
        show_profile()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=int(os.environ.get("PORT", 10000)), host="0.0.0.0")
