import flet as ft
import json, os

FILE = "mydata.json"
def load():
    if not os.path.exists(FILE): return {"user": None, "posts": []}
    try:
        with open(FILE,"r",encoding="utf-8") as f: return json.load(f)
    except: return {"user": None, "posts": []}

def save(d):
    with open(FILE,"w",encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False)

def main(page: ft.Page):
    page.title = "Apna Gaon"
    page.bgcolor = "black"
    page.padding = 0

    def show_upload_page(t):
        page.clean()
        caption = ft.TextField(label="Caption likho...", width=320, bgcolor="white", color="black", border_radius=12, multiline=True)
        file_name = ft.TextField(label=f"{t} File Name", width=320, bgcolor="white", color="black", border_radius=12, value=f"my_{t.lower()}.mp4")
        def do_final_upload(e):
            d = load(); d["posts"].append({"type": t, "file": file_name.value, "caption": caption.value})
            if d["user"]: d["user"]["posts_count"] = str(len(d["posts"]))
            save(d); show_profile()
        page.add(ft.Column([ft.Container(padding=15, content=ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda e: show_profile()), ft.Text(f"New {t}", color="white", size=18, weight="bold")])), ft.Container(padding=15, content=ft.Column([caption, file_name, ft.ElevatedButton(f"Upload {t}", on_click=do_final_upload, width=320, bgcolor="#d62976", color="white", height=50), ft.TextButton("Cancel", on_click=lambda e: show_profile())], spacing=15))], scroll=ft.ScrollMode.AUTO))

    def create_option(icon_name, text):
        def on_click(e):
            sheet.open=False; page.update(); show_upload_page(text)
        return ft.Container(padding=18, on_click=on_click, content=ft.Row([ft.Icon(icon_name, color="white", size=22), ft.Text(text, color="white", size=16)], spacing=15))

    sheet = ft.BottomSheet(bgcolor="#121212", content=ft.Column([ft.Container(padding=15, content=ft.Text("Create", color="white", size=20, weight="bold", text_align="center")), create_option(ft.Icons.VIDEO_LIBRARY, "Reel"), create_option(ft.Icons.GRID_ON, "Post"), create_option(ft.Icons.ADD_CIRCLE_OUTLINE, "Story"), ft.Container(height=20)], tight=True))
    page.overlay.append(sheet)
    def open_create(e): sheet.open=True; page.update()

    def show_profile():
        page.clean()
        d=load(); u=d["user"]
        if not u: show_register(); return
        posts=d.get("posts",[])
        posts_view=[]
        if not posts:
            posts_view.append(ft.Container(padding=30, content=ft.Column([ft.Icon(ft.Icons.CAMERA_ALT, color="grey", size=50), ft.Text("No Posts Yet", color="grey")], horizontal_alignment=ft.CrossAxisAlignment.CENTER)))
        else:
            for p in posts:
                posts_view.append(ft.Container(bgcolor="#1a1a1a", padding=12, border_radius=10, content=ft.Row([ft.Icon(ft.Icons.VIDEO_FILE if p["type"]=="Reel" else ft.Icons.IMAGE, color="white"), ft.Column([ft.Text(p["type"], color="white", weight="bold"), ft.Text(p.get("caption",""), color="grey", size=12)])])))
        page.add(ft.Column([ft.Container(padding=10, content=ft.Row([ft.IconButton(icon=ft.Icons.ADD, icon_color="white", on_click=open_create), ft.Text(u.get("username",""), color="white", size=20, weight="bold", expand=True), ft.Icon(ft.Icons.MENU, color="white")])), ft.Container(padding=15, content=ft.Row([ft.CircleAvatar(content=ft.Text(u.get("username","")[0].upper(), color="white", size=32), radius=42, bgcolor="#d62976"), ft.Row([ft.Column([ft.Text(u.get("posts_count","0"), color="white", weight="bold", size=18, text_align="center"), ft.Text("Posts", color="grey", size=12)], horizontal_alignment="center", expand=True), ft.Column([ft.Text(u.get("followers","0"), color="white", weight="bold", size=18, text_align="center"), ft.Text("Followers", color="grey", size=12)], horizontal_alignment="center", expand=True), ft.Column([ft.Text(u.get("following","0"), color="white", weight="bold", size=18, text_align="center"), ft.Text("Following", color="grey", size=12)], horizontal_alignment="center", expand=True)], expand=True, spacing=5)], spacing=15)), ft.Container(padding=ft.padding.only(left=15, right=15), content=ft.Column([ft.Text(u.get("name",""), color="white", weight="bold"), ft.Text("Welcome to Apna Gaon 🌾", color="white", size=13), ft.Row([ft.ElevatedButton("Edit profile", bgcolor="#262626", color="white", expand=True), ft.ElevatedButton("Share profile", bgcolor="#262626", color="white", expand=True)], spacing=8)], spacing=6)), ft.Divider(color="#262626"), ft.Column(posts_view, spacing=8)], scroll=ft.ScrollMode.AUTO, expand=True))

    def show_register():
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        uname = ft.TextField(label="Username", hint_text="apna naam likho", width=300, bgcolor="#121212", color="white", border_radius=12, border_color="#363636", prefix_icon=ft.Icons.PERSON_OUTLINE)
        pwd = ft.TextField(label="Password", hint_text="password", password=True, can_reveal_password=True, width=300, bgcolor="#121212", color="white", border_radius=12, border_color="#363636", prefix_icon=ft.Icons.LOCK_OUTLINE)

        def do_reg(e):
            if uname.value.strip()=="": return
            save({"user": {"username": uname.value.strip(), "password": pwd.value, "name": uname.value.strip(), "followers": "0", "following": "0", "posts_count": "0"}, "posts": []})
            show_profile()

        register_card = ft.Container(
            width=340,
            bgcolor="#0f0f0f",
            border_radius=20,
            padding=25,
            content=ft.Column([
                ft.Column([
                    ft.Container(width=70, height=70, border_radius=35, bgcolor="#d62976", content=ft.Text("A", color="white", size=35, weight="bold", text_align="center")),
                    ft.Text("Apna Gaon", color="white", size=28, weight="bold"),
                    ft.Text("Apno se judo, gaon se judo", color="grey", size=13, text_align="center"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                ft.Container(height=15),
                uname,
                pwd,
                ft.Container(height=10),
                ft.ElevatedButton("Register / Login", on_click=do_reg, width=300, height=48, bgcolor="#d62976", color="white"),
                ft.Text("Apna account banao aur Reel, Post share karo", color="grey", size=11, text_align="center"),
            ], spacing=12, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.add(ft.Column([register_card], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER))

    if not load()["user"]:
        show_register()
    else:
        show_profile()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=int(os.environ.get("PORT", 10000)), host="0.0.0.0")
