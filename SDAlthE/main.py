from pathlib import Path
import sys

file = Path(__file__).resolve()
parent, root = file.parent, file.parent.parent
sys.path.append(str(root))

from Scripts.interface import UI
from Scripts.core import configuration

#2476773268

window = UI.init_ui()
UI.menubar(window)
main_frame = UI.main_frame(window)
model = UI.model_combobox(main_frame)
main_notebook = UI.nootebook(main_frame)

# Text to Image:
txt2img = UI.notebook_frame(main_notebook, "txt2img")
image_frame, prompt_frame = UI.framebox_division(txt2img)
positive_prompt, negative_prompt = UI.prompt_text(prompt_frame)
image = UI.image_frame_show(image_frame)
UI.image_parameters_config(prompt_frame, window, image, model, positive_prompt, negative_prompt)

# Get Info:
get_info = UI.notebook_frame(main_notebook, "get_info")
info_image_frame, info_frame = UI.framebox_division(get_info)
image_get = UI.image_frame_show(info_image_frame)
UI.image_get_info(info_frame, image_get)
window.mainloop()