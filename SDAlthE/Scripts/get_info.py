from pathlib import Path
from PIL import Image, ImageTk
from tkinter import filedialog

def open_and_get(model, positive, negative, width_height, seed, steps, cfg, sampling_scheduler, image):
    file_path = Path(filedialog.askopenfilename(
        title="Selecione uma Imagem",
        filetypes=(("Image", "*.png"), ("All", "*.*")),
    ))

    with Image.open(file_path) as f:

        opened = ImageTk.PhotoImage(f)
        image.config(image=opened)
        image.image = opened

        info = f.info["paramethers"].split("~")
        
        modules = [model, positive, negative, width_height, seed, steps, cfg, sampling_scheduler]

        file_model = Path(info[0])
        model_name = file_model.stem

        info_all = [
            model_name
        ]

        for i in range(1, 3):
            info_all.append(info[i])
        info_all.append(f"{info[3]} / {info[4]}")
        for i in range(5, 8):
            info_all.append(info[i])
        info_all.append(f"{info[8]} / {info[9]}")

        for index in range(0, len(modules)):
            modules[index].config(state="normal")
            modules[index].delete(1.0, "end")
            modules[index].insert(1.0, info_all[index])
            modules[index].config(state="disabled")

