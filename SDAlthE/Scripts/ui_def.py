from pathlib import Path
import sys
import os
import subprocess

file = Path(__file__).resolve()
parent, root = file.parent, file.parent.parent
sys.path.append(str(root))

from Scripts.back import *
from Scripts.core import configuration

select_lang = load_language(configuration.get("language", "en"))

def restart():
    subprocess.Popen([sys.executable] + sys.argv)
    sys.exit()

def fullscreen(window):
    if window.state() == "zoomed":
        window.state("normal")
    else:
        window.state("zoomed")

def open_window_configuration(window):
    import ttkbootstrap as ttk

    window_configuration = ttk.Toplevel()
    window_configuration.title(language(select_lang, "window_config"))
    window_configuration.geometry("300x147")

    top = ttk.Frame(window_configuration)
    top.pack(fill="both")

    grid_gen(top, column=6)

    avaliable_resolution = configuration.get("avaliable_resolutions")
    possible_resolution = [possible.split("x")[0] for possible in avaliable_resolution]

    window.update_idletasks()
    window_resolution = window.geometry()
    real_resolution = window_resolution.split("+")[0]
    width = real_resolution.split("x")[0]

    if width in possible_resolution:
        index_resolution = possible_resolution.index(width)
        
    else:
        index_resolution = 0

    resolution_label = ttk.Label(top, text=language(select_lang, "resolution")+":")
    resolution_label.grid(row=0, column=2, pady=20)

    select_resolution = ttk.Combobox(top, values=avaliable_resolution, state="readonly", bootstyle="success")
    select_resolution.grid(row=0, column=3, pady=20)
    select_resolution.current(index_resolution)

    def save_resolution():
        window.geometry(select_resolution.get())
        window_configuration.destroy()

    confirm_resolution_button = ttk.Button(window_configuration, text=language(select_lang, "confirm"), command=save_resolution, bootstyle="success")

    if window.state() == "zoomed":
        select_resolution.configure(bootstyle="danger")

        not_work_label = ttk.Label(window_configuration, text=language(select_lang, "not_work_resolution"))
        not_work_label.pack()

        def not_work():
            window_configuration.destroy()
        confirm_not_work_button = ttk.Button(window_configuration, text=language(select_lang, "confirm"), command=not_work, bootstyle="danger")
        confirm_not_work_button.pack()
    else:
        confirm_resolution_button.pack()

def change_settings(window, new_language, new_theme):
    global configuration
    window.select_lang = load_language(new_language)
    configuration["language"] = new_language
    configuration["style"] = new_theme
    json_save("configuration.json", configuration)
    restart()
    
def open_configuration(window, root_directory):
    import ttkbootstrap as ttk

    configuration_window = ttk.Toplevel()
    configuration_window.title(language(select_lang, "configuration"))
    configuration_window.geometry("360x300")

    top = ttk.Frame(configuration_window)
    top.pack(fill="both")

    grid_gen(top, column=6, row=1)

    top.rowconfigure(0, weight=0, minsize=20)
    top.rowconfigure(2, weight=0, minsize=20)
    top.rowconfigure(4, weight=0, minsize=20)

    theme_list = configuration.get("avaliable_styles")
    list_language = language_list(root_directory)

    language_index = list_language.index(configuration.get("language"))
    style_index =  theme_list.index(configuration.get("style"))

    language_label = ttk.Label(top, text=language(select_lang, "language")+":")
    language_label.grid(column=2, row=1, sticky="e")

    language_combobox = ttk.Combobox(top, values=list_language, state="readonly", bootstyle="info")
    language_combobox.grid(column=3, row=1, sticky="w")
    language_combobox.current(language_index)

    theme_label = ttk.Label(top, text=language(select_lang, "theme")+":")
    theme_label.grid(column=2, row=3, sticky="e")

    theme_combobox = ttk.Combobox(top, values=theme_list, state="readonly", bootstyle="info")
    theme_combobox.grid(column=3, row=3, sticky="w")
    theme_combobox.current(style_index)

    warning_label = ttk.Label(configuration_window, text=language(select_lang, "settings_warning"))
    warning_label.pack()
    confirm_button = ttk.Button(configuration_window, text=language(select_lang, "confirm"), bootstyle="warning", command=lambda: change_settings(window, language_combobox.get(), theme_combobox.get()))
    confirm_button.pack()