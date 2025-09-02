import json
import subprocess
import tkinter as tk
from tkinter import messagebox
import os
import tempfile
import threading
import winshell
from win32com.client import Dispatch

#! Config stored in %APPDATA%/houseoffun/fivem_launcher/config.json
APPDATA = os.getenv('APPDATA') or os.path.expanduser('~')
CONFIG_DIR = os.path.join(APPDATA, 'houseoffun/fivem_launcher')
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.json')

DEFAULT_CONFIG = {
    "fivem_path": "",
    "servers": [
        {
            "name": "Dev Server",
            "connection": "127.0.0.1:30120",
            "pure_mode": 1,
            "gamebuild": 2060,
            "type": "dev"
        },
        {
            "name": "Live Server",
            "connection": "cfx.re/join/abcd1234",
            "pure_mode": 2,
            "gamebuild": 2189,
            "type": "play"
        }
    ],
    "cl2": False, #? Set to true if you want the CL2 button to appear, you also must have one, and only one, server listed as type: "dev"
    "local_server": {
        "fxserver_path": ""
    }
}

def load_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_PATH):
        #? Autodetect fivem location
        possible_fivem = os.path.join(APPDATA, 'Local', 'FiveM', 'FiveM.exe')
        config = DEFAULT_CONFIG.copy()
        if os.path.exists(possible_fivem):
            config["fivem_path"] = possible_fivem
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
        return config
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def launch_fivem(fivem_path, connection, pure_mode, gamebuild):
    try:
        #? Put together arg string
        args = []
        if pure_mode:
            args.append(f"-pure_{pure_mode}")
        if gamebuild:
            args.append(f"-b{gamebuild}")
        if connection:
            args.append(f"-connect {connection}")
        
        #? Cheeky workaround since fivem doesn't like being launched directly from a non-shell subprocess
        shell = Dispatch('WScript.Shell')
        shortcut_path = os.path.join(tempfile.gettempdir(), f"fivem_launch_{os.getpid()}.lnk")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = fivem_path
        shortcut.Arguments = " ".join(args)
        shortcut.WorkingDirectory = os.path.dirname(fivem_path)
        shortcut.save()
        
        subprocess.Popen(['explorer.exe', shortcut_path], shell=False)
        
        #? Delete temp shortcut file after delay
        def cleanup():
            import time
            time.sleep(15)
            try:
                os.unlink(shortcut_path)
            except:
                pass
        threading.Thread(target=cleanup, daemon=True).start()
        
    except Exception as e:
        #? Fallbacks if main workaround method fails
        try:
            if not any([pure_mode, gamebuild, connection]):
                subprocess.Popen(['explorer.exe', fivem_path], shell=False)
            else:
                cmd = f'start "" "{fivem_path}" {" ".join(args)}'
                subprocess.Popen(['cmd.exe', '/c', cmd], shell=False, creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e2:
            messagebox.showerror("Error", f"Failed to launch FiveM: {e2}\n\nOriginal error: {e}")

def main():
    #! State Management
    state = {}
    def update_state(new_config=None):
        if new_config is None:
            new_config = load_config()
        state["config"] = new_config
        state["fivem_path"] = new_config.get("fivem_path", "fivem.exe")
        state["servers"] = new_config.get("servers", [])
        state["dev_server"] = None
        for server in state["servers"]:
            if server.get("type") == "dev":
                state["dev_server"] = server
                break
    update_state()

    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)

    window_width = 220
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    #? Theme
    bg_color = "#222"
    fg_color = "#eee"
    accent_color = "#444"
    select_bg = "#555"
    select_fg = "#fff"
    topbar_color = "#333"
    btn_color = "#222"
    btn_hover = "#555"

    root.configure(bg=bg_color)

    #? Title Bar (Edit, Refresh, Close)
    topbar = tk.Frame(root, bg=topbar_color, height=28)
    topbar.pack(fill=tk.X, side=tk.TOP)

    #? Moving window logic
    def start_move(event):
        root.x = event.x
        root.y = event.y
    def stop_move(event):
        root.x = None
        root.y = None
    def do_move(event):
        x = root.winfo_pointerx() - root.x
        y = root.winfo_pointery() - root.y
        root.geometry(f"220x200+{x}+{y}")
    topbar.bind('<Button-1>', start_move)
    topbar.bind('<ButtonRelease-1>', stop_move)
    topbar.bind('<B1-Motion>', do_move)

    #? Action buttons
    btn_style = {'bg': btn_color, 'fg': fg_color, 'activebackground': btn_hover, 'activeforeground': fg_color, 'bd': 0, 'width': 3, 'height': 1, 'font': ('Arial', 10, 'bold')}
    def on_close():
        root.destroy()
    def on_edit():
        try:
            os.startfile(CONFIG_PATH)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open config: {e}")
    def on_refresh():
        new_config = load_config()
        update_state(new_config)
        listbox.delete(0, tk.END)
        for server in state["servers"]:
            display = f"  {server['name']}  "
            listbox.insert(tk.END, display)
        render_buttons()

    btn_close = tk.Button(topbar, text='✕', command=on_close, **btn_style)
    btn_close.pack(side=tk.RIGHT, padx=0)
    btn_refresh = tk.Button(topbar, text='⟳', command=on_refresh, **btn_style)
    btn_refresh.pack(side=tk.RIGHT, padx=0)
    btn_edit = tk.Button(topbar, text='✎', command=on_edit, **btn_style)
    btn_edit.pack(side=tk.RIGHT, padx=0)

    #? Listbox
    listbox = tk.Listbox(root, font=("Arial", 11, "bold"), bg=accent_color, fg=fg_color,
                        selectbackground=select_bg, selectforeground=select_fg,
                        highlightbackground=bg_color, highlightcolor=accent_color,
                        bd=0, relief=tk.FLAT, activestyle='none', height=len(state["servers"]))
    for server in state["servers"]:
        display = f"  {server['name']}  "
        listbox.insert(tk.END, display)
    listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,4))

    def on_select(event):
        idx = listbox.curselection()
        if not idx:
            return
        server = state["servers"][idx[0]]
        launch_fivem(
            state["fivem_path"],
            server.get("connection"),
            server.get("pure_mode"),
            server.get("gamebuild")
        )

    listbox.bind('<<ListboxSelect>>', on_select)

    #? Bottom Buttons (use frames for easy update)
    button_frame = tk.Frame(root, bg=bg_color)
    button_frame.pack(fill=tk.X, side=tk.BOTTOM)

    def render_buttons():
        for widget in button_frame.winfo_children():
            widget.destroy()

        #? Launch local server button
        local_server_path = state["config"].get("local_server", {}).get("fxserver_path", "")
        def launch_local_server():
            if local_server_path:
                try:
                    subprocess.Popen(['explorer.exe', local_server_path], shell=False)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to launch local server: {e}")
            else:
                messagebox.showwarning("Not Configured", "Local server path not set in config.json.")
        if local_server_path:
            local_btn = tk.Button(button_frame, text="Launch Local Server", font=("Arial", 10, "bold"),
                                bg=accent_color, fg=fg_color, activebackground=select_bg, activeforeground=select_fg,
                                bd=0, relief=tk.FLAT, command=launch_local_server)
            local_btn.pack(fill=tk.X, padx=8, pady=(0,4))

        #? cl2 logic
        if state["config"].get("cl2", False) and state["dev_server"]:
            def launch_cl2():
                try:
                    args = ["-cl2"]
                    dev_server = state["dev_server"]
                    if dev_server.get("pure_mode"):
                        args.append(f"-pure_{dev_server['pure_mode']}")
                    if dev_server.get("gamebuild"):
                        args.append(f"-b{dev_server['gamebuild']}")
                    if dev_server.get("connection"):
                        args.append(f"-connect {dev_server['connection']}")

                    #? Same workaround for cl2
                    shell = Dispatch('WScript.Shell')
                    shortcut_path = os.path.join(tempfile.gettempdir(), f"fivem_cl2_{os.getpid()}.lnk")
                    shortcut = shell.CreateShortCut(shortcut_path)
                    shortcut.Targetpath = state["fivem_path"]
                    shortcut.Arguments = " ".join(args)
                    shortcut.WorkingDirectory = os.path.dirname(state["fivem_path"])
                    shortcut.save()
                    
                    subprocess.Popen(['explorer.exe', shortcut_path], shell=False)
                    
                    def cleanup():
                        import time
                        time.sleep(15)
                        try:
                            os.unlink(shortcut_path)
                        except:
                            pass
                    threading.Thread(target=cleanup, daemon=True).start()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to launch FiveM with -cl2: {e}")
            cl2_btn = tk.Button(button_frame, text="Launch Second Client (-cl2)", font=("Arial", 10, "bold"),
                                bg=accent_color, fg=fg_color, activebackground=select_bg, activeforeground=select_fg,
                                bd=0, relief=tk.FLAT, command=launch_cl2)
            cl2_btn.pack(fill=tk.X, padx=8, pady=(0,4))

        #? Launch button with no params
        launch_btn = tk.Button(button_frame, text="Launch Fivem (No Params)", font=("Arial", 10, "bold"),
            bg=accent_color, fg=fg_color, activebackground=select_bg, activeforeground=select_fg,
            bd=0, relief=tk.FLAT, command=lambda: launch_fivem(state["fivem_path"], None, None, None))
        launch_btn.pack(fill=tk.X, padx=8, pady=(0,8))

    render_buttons()

    root.mainloop()

if __name__ == "__main__":
    main()
