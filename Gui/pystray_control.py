import pystray
from PIL import Image, ImageDraw
from .gui_display import refresh_display

def create_image():
    image = Image.new('RGB', (64, 64), (0, 128, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle([8, 8, 56, 56], fill='white')
    return image

def show_window():
    if not root.winfo_viewable():
        root.deiconify()
    else:
        root.lift()

def hide_window():
    root.withdraw()

def on_quit(icon, item):
    icon.stop()
    root.destroy()

# Create the icon and menu
icon = pystray.Icon(
    "test_icon",
    icon=create_image(),
    title="My Tray App",
    menu=pystray.Menu(
        pystray.MenuItem("Quit", on_quit),
        pystray.MenuItem("Open command table", refresh_display)
    )
)

icon.run()