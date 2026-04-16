from pathlib import Path
import sys

file = Path(__file__).resolve()
parent, root = file.parent, file.parent.parent
sys.path.append(str(root))

from Scripts.interface import UI

#2476773268

window = UI.init_ui()
UI.menubar(window)
main_frame = UI.main_frame(window)
model = UI.model_combobox(main_frame)
main_notebook = UI.nootebook(main_frame)


# Text to Image:
txt2img = UI.notebook_frame(main_notebook, "txt2img")
scroll_t2i = UI.scrollable_frame(txt2img)
image_frame, prompt_frame = UI.framebox_division(scroll_t2i)
positive_prompt, negative_prompt = UI.prompt_text(prompt_frame)
image = UI.image_frame_show(image_frame)
UI.image_parameters_config(prompt_frame, window, image, model, positive_prompt, negative_prompt, "txt2img")


# Image to Image
img2img = UI.notebook_frame(main_notebook, "img2img")
scroll_i2i = UI.scrollable_frame(img2img)
image_frame_i2i, prompt_frame_i2i = UI.framebox_division(scroll_i2i)
positive_i2i, negative_i2i, base_image = UI.prompt_img2img(prompt_frame_i2i)
image_i2i = UI.image_frame_show(image_frame_i2i)
UI.image_parameters_config(prompt_frame_i2i, window, image_i2i, model, positive_i2i, negative_i2i, "img2img", base_image)


# Get Info:
get_info = UI.notebook_frame(main_notebook, "get_info")
scroll_info = UI.scrollable_frame(get_info)
info_image_frame, info_frame = UI.framebox_division(scroll_info)
image_get = UI.image_frame_show(info_image_frame)
UI.image_get_info(info_frame, image_get)
window.mainloop()