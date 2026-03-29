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
        
        module = [model, positive, negative, width_height, seed, steps, cfg, sampling_scheduler]

        file_model = Path(info[0])
        model_name = file_model.stem
        module[0].config(state="normal")
        module[0].delete(1.0, "end")
        module[0].insert(1.0, model_name)
        module[0].config(state="disabled")

        module[1].config(state="normal")
        module[1].delete(1.0, "end")
        module[1].insert(1.0, info[1])
        module[1].config(state="disabled")

        module[2].config(state="normal")
        module[2].delete(1.0, "end")
        module[2].insert(1.0, info[2])
        module[2].config(state="disabled")

        module[3].config(state="normal")
        module[3].delete(1.0, "end")
        module[3].insert(1.0, f"{info[3]} / {info[4]}")
        module[3].config(state="disabled")

        module[4].config(state="normal")
        module[4].delete(1.0, "end")
        module[4].insert(1.0, info[5])
        module[4].config(state="disabled")

        module[5].config(state="normal")
        module[5].delete(1.0, "end")
        module[5].insert(1.0, info[6])
        module[5].config(state="disabled")

        module[6].config(state="normal")
        module[6].delete(1.0, "end")
        module[6].insert(1.0, info[7])
        module[6].config(state="disabled")

        module[7].config(state="normal")
        module[7].delete(1.0, "end")
        module[7].insert(1.0, f"{info[8]} / {info[9]}")
        module[7].config(state="disabled")