from tkinter import *
from PIL import Image, ImageTk
from pathlib import Path
import sys
import ttkbootstrap as ttk
import threading

file = Path(__file__).resolve()
parent, root = file.parent, file.parent.parent
sys.path.append(str(root))

from Scripts.ui_def import *
from Scripts.core import configuration, Image_Generation
from Scripts.get_info import *

# --------------------------------------------------------------

rdir = root_dir()
assets_dir = rdir / "Assets"

class UI:

    width = None
    height = None
    resolution = None
    select_lang = None

    @classmethod
    def init_ui(cls) -> Tk:

        window = Tk()

        cls.width = window.winfo_screenwidth()
        cls.height = window.winfo_screenheight()
        cls.resolution = f"{cls.width}x{cls.height}"

        icon = ttk.PhotoImage(file=assets_dir / "icone.png")
        window.iconphoto(True, icon)
        window.title("Stable Alth Diffussion")
        window.geometry(cls.resolution)
        window.state("zoomed")
        ttk.Style(configuration.get("style", "darkly").lower().split(" ")[1])

        cls.select_lang = load_language(configuration.get("language", "pt"))

        cls.init = True

        return window
        
    @classmethod
    def menubar(cls, window: Tk):

        menu_bar = ttk.Menu(window)
        window.config(menu=menu_bar)

        config_menu = ttk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=language(cls.select_lang, "tools"), menu=config_menu)
        config_menu.add_command(label=language(cls.select_lang, "personalization"), command=lambda: open_configuration(window, rdir))

        window_menu = ttk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=language(cls.select_lang, "window"), menu=window_menu)
        window_menu.add_command(label=language(cls.select_lang, "fullscreen"), command=lambda: fullscreen(window))
        window_menu.add_command(label=language(cls.select_lang, "window_config"), command=lambda: open_window_configuration(window))

    @staticmethod
    def main_frame(window: Tk) -> ttk.Frame:
        frame = ttk.Frame(window)
        frame.pack(fill="both")

        frame.rowconfigure(0, weight=0, minsize=20)
        frame.rowconfigure(1, weight=0, minsize=20)
        frame.rowconfigure(2, weight=1, minsize=30)
        frame.columnconfigure(0, weight=0 ,minsize=20)
        frame.columnconfigure(1, weight=1, minsize=20)
        frame.columnconfigure(2, weight=0, minsize=20)
        frame.rowconfigure(3, weight=0, minsize=20)
        frame.rowconfigure(4, weight=1, minsize=20)

        return frame
    @classmethod
    def model_combobox(cls, frame: ttk.Frame) -> ttk.Combobox:
        information_label = Label(frame, text=language(cls.select_lang, "checkpoint_info")+":", width=60)
        information_label.grid(row=1, column=1, sticky="nw")
        model_list = list(list_model())
        model_combobox = ttk.Combobox(frame, values=model_list, width=60, state="readonly", bootstyle="light")
        model_combobox.grid(row=2, column=1, sticky="nw")
        model_combobox.current(0)

        device_label = ttk.Label(frame, text=language(cls.select_lang, "device")+":", width=60)
        device_label.grid(row=1, column=1, sticky="ne")
        devices = ["CUDA", f"CPU"+"("+language(cls.select_lang, "working_progress")+")"]
        device_combo = ttk.Combobox(frame, values=devices, width=60, state="readonly", bootstyle="success")
        device_combo.grid(row=2, column=1, sticky="ne")
        device_combo.current(0)

        device_model = [model_combobox, device_combo]

        return device_model

    @classmethod
    def nootebook(cls, frame: ttk.Frame) -> ttk.Notebook:
        notebook = ttk.Notebook(frame, bootstyle="secondary")
        notebook.grid(row=4, column=1, sticky="nsew")

        return notebook

    @classmethod
    def notebook_frame(cls, notebook: ttk.Notebook, title: str) -> ttk.Frame:
        notebook_frame = ttk.Frame(notebook)
        notebook.add(notebook_frame, text=language(cls.select_lang, title))

        return notebook_frame
    
    @classmethod
    def framebox_division(cls, notebook_frame: ttk.Frame) -> tuple[ttk.Frame, ttk.Frame]:
        notebook_frame.rowconfigure(0, weight=1)
        notebook_frame.columnconfigure(0, weight=1)
        notebook_frame.columnconfigure(1, weight=1)

        image_frame = Frame(notebook_frame)
        prompt_frame = Frame(notebook_frame)
        prompt_frame.grid(row=0, column=0, sticky="nw")
        image_frame.grid(row=0, column=1)

        return image_frame, prompt_frame
    
    @classmethod
    def prompt_text(cls, frame: ttk.Frame) -> tuple[ttk.Text, ttk.Text]:

        frame.rowconfigure(0, weight=0, minsize=20)
        frame.columnconfigure(0, weight=0, minsize=20)
        frame.columnconfigure(1, weight=1, minsize=20)
        frame.rowconfigure(1, weight=1, minsize=20)
        frame.rowconfigure(2, weight=1, minsize=30)
        frame.rowconfigure(3, weight=0, minsize=20)
        frame.rowconfigure(4, weight=1, minsize=20)
        frame.rowconfigure(5, weight=1, minsize=30)
        frame.columnconfigure(100, weight=0, minsize=20)

        positive_label = Label(frame, text=language(cls.select_lang, "positive_prompt_label")+":")
        positive_label.grid(row=1, column=1, sticky="nw")
        positive_prompt = ttk.Text(frame, width=100, height=6)
        positive_prompt.grid(row=2, column=1, sticky="nw")
        
        negative_label = Label(frame, text=language(cls.select_lang, "negative_prompt_label")+":")
        negative_label.grid(row=4, column=1, sticky="nw")
        negative_prompt = ttk.Text(frame, width=100, height=6)
        negative_prompt.grid(row=5, column=1, sticky="nw")

        return positive_prompt, negative_prompt
    
    @classmethod
    def image_parameters_config(cls, frame: ttk.Frame, window: Tk, label: ttk.Label, model, positive, negative) -> dict:
        gen_config = Frame(frame)
        gen_config.grid(row=6, column=1)

        gen_config.rowconfigure(0, weight=0, minsize=40)
        gen_config.rowconfigure(1, weight=1)
        gen_config.rowconfigure(2, weight=1)
        gen_config.rowconfigure(3, weight=0, minsize=20)
        gen_config.rowconfigure(6, weight=0, minsize=20)
        gen_config.rowconfigure(9, weight=0, minsize=20)
        gen_config.rowconfigure(12, weight=0, minsize=20)
        gen_config.rowconfigure(14, weight=0, minsize=20)
        gen_config.columnconfigure(0, weight=1)
        gen_config.columnconfigure(1, weight=0, minsize=20)
        gen_config.columnconfigure(2, weight=1)
        gen_config.columnconfigure(3, weight=0, minsize=20)

        sampling_label = Label(gen_config, text=language(cls.select_lang, "sampling_method")+":")
        sampling_label.grid(row=1, column=0, sticky="n")

        sampling_list = ["DDIM", "DPM++ 2M", "DPM++ SDE", "Euler", "Euler A", "LMS", "Heun", "UniPC"]
        sampling_method = ttk.Combobox(gen_config, values=sampling_list, state="readonly", width=45, bootstyle="secondary")
        sampling_method.grid(row=2, column=0, sticky="n")
        sampling_method.current(0)

        schedule_type_label = Label(gen_config, text=language(cls.select_lang, "schedule_type")+":")
        schedule_type_label.grid(row=1, column=2, sticky="n")

        schedule_type_list = ["Automatic", "Karras"]
        schedule_type = ttk.Combobox(gen_config, values=schedule_type_list, state="readonly", width=45, bootstyle="secondary")
        schedule_type.grid(row=2, column=2, sticky="n")
        schedule_type.current(0)

        def when_move_w(v):
            width_value.set(int(float(v)))

        def when_move_h(v):
            height_value.set(int(float(v)))

        width_value = ttk.IntVar(value=512)
        height_value = ttk.IntVar(value=512)

        width_label = Label(gen_config, text=language(cls.select_lang, "width")+":")
        width_label.grid(row=4, column=0, sticky="nw")

        height_label = Label(gen_config, text=language(cls.select_lang, "height")+":")
        height_label.grid(row=4, column=2, sticky="nw")

        image_width = ttk.Spinbox(gen_config, from_=64, to=2048, increment=8, textvariable=width_value)
        image_width.grid(row=4, column=0, sticky="ne")

        image_height = ttk.Spinbox(gen_config, from_=64, to=2048, increment=8, textvariable=height_value)
        image_height.grid(row=4, column=2, sticky="ne")

        image_width_scale = ttk.Scale(gen_config, from_=64, to=2048, orient="horizontal", variable=width_value, length=300, command=when_move_w)
        image_width_scale.grid(row=5, column=0)

        image_height_scale = ttk.Scale(gen_config, from_=64, to=2048, orient="horizontal", variable=height_value, length=300, command=when_move_h)
        image_height_scale.grid(row=5, column=2)

        def when_move(v):
            steps_value.set(int(float(v)))

        steps_value = ttk.IntVar(value=20)

        steps_label = Label(gen_config, text=language(cls.select_lang, "sampling_steps")+":")
        steps_label.grid(row=7, column=0, sticky="nw")

        steps_box = ttk.Spinbox(gen_config, from_=1, to=150, increment=1, textvariable=steps_value)
        steps_box.grid(row=7, column=0, sticky="ne")

        steps_scale = ttk.Scale(gen_config, from_=1, to=150, orient="horizontal", variable=steps_value, length=300, command=when_move)
        steps_scale.grid(row=8, column=0)

        def cfg_move(v):
            v = float(v)
            v = round(v * 2) / 2
            cfg_value.set(v)

        cfg_value = ttk.DoubleVar(value=7.0)

        cfg_text = Label(gen_config, text=language(cls.select_lang, "cfg_scale")+":")
        cfg_text.grid(row=7, column=2, sticky="nw")

        cfg_box = ttk.Spinbox(gen_config, from_=1, to=30, increment=0.5, textvariable=cfg_value)
        cfg_box.grid(row=7, column=2, sticky="ne")

        cfg = ttk.Scale(gen_config, from_=1, to=30, orient="horizontal", variable=cfg_value, length=300, command=cfg_move)
        cfg.grid(row=8, column=2)

        vcmd = window.register(validate_seed)

        seed_value = StringVar()

        seed_label = Label(gen_config, text=language(cls.select_lang, "seed")+":")
        seed_label.grid(row=10, column=0, sticky="nw")

        entry_seed = ttk.Entry(gen_config, validate="key", validatecommand=(vcmd, "%P"), textvariable=seed_value, width=47)
        entry_seed.grid(row=11, column=0, sticky="nw")

        """recycle = ttk.Button(gen_config, text=language(cls.select_lang, "recycle_seed"))
        recycle.grid(row=11, column=2, sticky="n")"""

        random_seed(seed_value)

        random_seed_button = ttk.Button(gen_config, text=language(cls.select_lang, "random"), command=lambda: random_seed(seed_value))
        random_seed_button.grid(row=11, column=2, sticky="nw")

        def update_image(image, image_box: Label, button: ttk.Button):
            generated = ImageTk.PhotoImage(image)
            image_box.config(image=generated)
            image_box.image = generated
            button.config(state="normal")

        def worker(paramethers, image_box, button):
            try:
                generated = Image_Generation.generate_image(paramethers)

                save_image(generated, paramethers)

                image_box.after(0, update_image, generated, image_box, button)
            except Exception as e:
                print(e)
                button.config(state="normal")


        def image_generation_button(image_box: Label, button: ttk.Button):
            button.config(state="disabled")

            if seed_value.get() == "":
                random_seed(seed_value)

            paramethers = {
                "positive": positive.get(1.0,END).strip(),
                "negative": negative.get(1.0,END).strip(),
                "model": list_model().get(model[0].get()),
                "sampler": sampling_method.get(),
                "scheduler": schedule_type.get(),
                "width": width_value.get(),
                "height": height_value.get(),
                "steps": steps_value.get(),
                "seed": seed_value.get(),
                "cfg": cfg_value.get(),
                "device": model[1].get().lower()
            }
            thread = threading.Thread(
                target=worker,
                args=(paramethers, image_box, button)
            )
            thread.start()


        gen_button = ttk.Button(gen_config, text=language(cls.select_lang, "generate"), command=lambda: image_generation_button(label, gen_button))
        gen_button.grid(row=13, column=0)

    @classmethod
    def image_frame_show(cls, frame: ttk.Frame):
        frame_image_dir = assets_dir / "image frame.png"
        frame_image = Image.open((frame_image_dir))
        frame_image = frame_image.resize((500, 500))
        img_tk = ImageTk.PhotoImage(frame_image)
        image_label = Label(frame, image=img_tk)
        image_label.pack()
        image_label.image = img_tk

        return image_label

    @classmethod
    def image_get_info(cls, frame, image):

        frame.rowconfigure(0, weight=0, minsize=20)
        frame.rowconfigure(2, weight=0, minsize=20)
        frame.rowconfigure(5, weight=0, minsize=20)
        frame.rowconfigure(8, weight=0, minsize=20)
        frame.rowconfigure(11, weight=0, minsize=20)
        frame.rowconfigure(14, weight=0, minsize=20)
        frame.rowconfigure(17, weight=0, minsize=20)
        frame.rowconfigure(20, weight=0, minsize=20)
        frame.rowconfigure(23, weight=0, minsize=20)
        frame.rowconfigure(26, weight=0, minsize=20)
        frame.columnconfigure(0, weight=0, minsize=20)

        model_label = ttk.Label(frame, text=language(cls.select_lang, "model")+":")
        model_label.grid(row=3, column=1, sticky="nw")
        model_entry = ttk.Text(frame, state="disabled", width=100, height=1)
        model_entry.grid(row=4, column=1)

        positive_label = ttk.Label(frame, text=language(cls.select_lang, "positive_prompt_label")+":")
        positive_label.grid(row=6, column=1, sticky="nw")
        positive_prompt = ttk.Text(frame, width=100, height=6, state="disabled",)
        positive_prompt.grid(row=7, column=1, sticky="nw")

        negative_label = ttk.Label(frame, text=language(cls.select_lang, "negative_prompt_label")+":")
        negative_label.grid(row=9, column=1, sticky="nw")
        negative_prompt = ttk.Text(frame, width=100, height=6, state="disabled")
        negative_prompt.grid(row=10, column=1, sticky="nw")

        width_height_label = ttk.Label(frame, text=language(cls.select_lang, "width_height"))
        width_height_label.grid(row=12, column=1, sticky="nw")
        width_height_entry = ttk.Text(frame, state="disabled", width=100, height=1)
        width_height_entry.grid(row=13, column=1)

        seed_label = ttk.Label(frame, text=language(cls.select_lang, "seed")+":")
        seed_label.grid(row=15, column=1, sticky="nw")
        seed_entry = ttk.Text(frame, state="disabled", width=100, height=1)
        seed_entry.grid(row=16, column=1)

        steps_label = ttk.Label(frame, text=language(cls.select_lang, "sampling_steps")+":")
        steps_label.grid(row=18, column=1, sticky="nw")
        steps_entry = ttk.Text(frame, state="disabled", width=100, height=1)
        steps_entry.grid(row=19, column=1)

        cfg_label = ttk.Label(frame, text=language(cls.select_lang, "cfg_scale")+":")
        cfg_label.grid(row=21, column=1, sticky="nw")
        cfg_entry = ttk.Text(frame, state="disabled", width=100, height=1)
        cfg_entry.grid(row=22, column=1)

        sampling_scheduler_label = ttk.Label(frame, text=language(cls.select_lang, "sampling_scheduler")+":")
        sampling_scheduler_label.grid(row=24, column=1, sticky="nw")
        sampling_scheduler_entry = ttk.Text(frame, state="disabled", width=100, height=1)
        sampling_scheduler_entry.grid(row=25, column=1)

        image_select = ttk.Button(frame, text=language(cls.select_lang, "open_image"), bootstyle="success", command=lambda: open_and_get(model_entry, positive_prompt, negative_prompt, width_height_entry, seed_entry, steps_entry, cfg_entry, sampling_scheduler_entry, image))
        image_select.grid(row=1, column=1)