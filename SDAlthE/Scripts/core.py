from pathlib import Path
import sys

file = Path(__file__).resolve()
parent, root = file.parent, file.parent.parent
sys.path.append(str(root))
from Scripts.back import *

class Image_Generation:

    #actual_model = None

    @classmethod
    def generate_image(cls, info: dict, generation, progress, image_base=None, strength=None):
        from compel import Compel

        from Scripts.pipeline_core import Stable_Diffusion_Core as SD

        SD.pipeline_init(info.get("model"), generation)

        SD.pipe.to(info.get("device"))

        generator = SD.generator_seed(int(info.get("seed")), info.get("device"))

        #positive_prompts = SD.encode_prompts(SD.pipe, info.get("positive"))
        #negative_prompts = SD.encode_prompts(SD.pipe, info.get("negative"))

        positive, loras = SD.loras_indentification(info.get("positive"))
        try:
            SD.pipe.unload_lora_weights()
        except Exception:
            pass

        avaliable_loras = list_loras()

        for lora, weight in loras:
            lora_path = avaliable_loras.get(lora)
            if not lora_path:
                print(f"Lora {lora} não encontrado.")
                continue

            SD.pipe.load_lora_weights(str(lora_path), adapter_name=lora)

            if loras:
                adapter_names = [name for name, _ in loras if name in avaliable_loras]
                adapter_weights = [weight for name, weight in loras if name in avaliable_loras]

                if adapter_names:
                    SD.pipe.set_adapters(adapter_names, adapter_weights=adapter_weights)

        compel = Compel(
            tokenizer=SD.pipe.tokenizer,
            text_encoder=SD.pipe.text_encoder
        )

        positive_embeds = compel(positive)
        negative_embeds = compel(info.get("negative"))

        #positive_embeds, negative_embeds = SD.pad_to_match(positive_prompts, negative_prompts)


        if info.get("scheduler") == "Karras":
            use_karras = True
        else:
            use_karras = False

        progress["maximum"] = int(info.get("steps"))
        progress["value"] = 0
        progress.config(bootstyle="warning")

        def callback(pipeline, step_index, timestep, callback_kargs):
            progress["value"] = step_index + 1
            return callback_kargs

        SD.sampler_define(SD.pipe, info.get("sampler"), use_karras)

        if generation == "txt2img" or image_base == None:

            image = SD.image_generate(
                pipe=SD.pipe,
                pos_embeds=positive_embeds,
                neg_embeds=negative_embeds,
                generator=generator,
                steps=int(info.get("steps")),
                cfg=int(info.get("cfg")),
                width=int(info.get("width")),
                height=int(info.get("height")),
                callback=callback
            )
        elif generation == "img2img":
            rgb_image = Image.open(image_base.get()).convert("RGB")

            image = SD.image_generate_by_image(
                pipe=SD.pipe,
                pos_embeds=positive_embeds,
                neg_embeds=negative_embeds,
                generator=generator,
                steps=int(info.get("steps")),
                cfg=int(info.get("cfg")),
                width=int(info.get("width")),
                height=int(info.get("height")),
                image_base=rgb_image,
                callback=callback,
                strength=strength
            )

        return image