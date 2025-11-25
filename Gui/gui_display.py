import tkinter as tk
import pystray
from PIL import Image, ImageDraw
from actions.action_files.database import get_mode
import json, os
import threading

base_dir = os.path.dirname(__file__)
macro_path = os.path.join(base_dir, "../config/macros.json")

with open(macro_path) as f:
    macros = json.load(f)

def refresh_display():
    mode = get_mode()
    commands = "\n".join(macros.get(mode, {}).keys())
    mode_label.config(text=f"Current Mode: {mode}")
    commands_box.delete(0, tk.END)
    for cmd in macros.get(mode, {}).keys():
        commands_box.insert(tk.END, cmd)


    root.update_idletasks()
    
     # Get total desired window size (not just listbox)
    w = root.winfo_reqwidth()
    h = root.winfo_reqheight()

    # Apply padding and cap height if needed
    padding = 30  # ensures bottom button stays visible
    h = min(h + padding, 500)

    screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
    x = screen_w - w - 20
    y = screen_h - h - 60
    root.geometry(f"{w}x{h}+{x}+{y}")

def create_image():
    icon_path = os.path.join(base_dir,"assets/headset.png")
    try:
        return Image.open(icon_path)
    except FileNotFoundError:
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

root = tk.Tk()
root.overrideredirect(True)
# root.attributes("-topmost", True) 
# root.attributes("-alpha", 0.95) 
# root.title("Voice Assistant Dashboard")

# width, height = 300, 180
# root.update_idletasks()
# screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
# x, y = screen_w - width - 20, screen_h - height - 60
# root.geometry(f"{width}x{height}+{x}+{y}")

mode_label = tk.Label(root, text="Current Mode:", font=("Arial", 16))
mode_label.pack(pady=10)

commands_box = tk.Listbox(root, font=("Consolas", 12), activestyle="none", borderwidth=0, highlightthickness=0)
commands_box.pack(padx=10, pady=5, fill="both", expand=True)

refresh_btn = tk.Button(root, text="Refresh", command=refresh_display)
refresh_btn.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=hide_window)
exit_button.pack(pady=5)

refresh_display()
root.withdraw()

def setup_tray():
    menu = pystray.Menu(
        pystray.MenuItem("Open command table", show_window),
        pystray.MenuItem("Quit", on_quit)
        
    )
    
    icon = pystray.Icon("assistant_tray", create_image(), "Voice Assistant", menu)
    icon.run()

threading.Thread(target=setup_tray, daemon=True).start()
root.mainloop()

# if __name__ == "__main__":
#     refresh_display()