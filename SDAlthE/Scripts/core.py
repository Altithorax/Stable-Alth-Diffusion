from pathlib import Path
import sys

file = Path(__file__).resolve()
parent, root = file.parent, file.parent.parent
sys.path.append(str(root))
from Scripts.back import *

configuration = json_load("configuration.json")

class Image_Generation:

    pipeline_initialized = False

    @classmethod
    def generate_image(cls, info: dict):
        from compel import Compel

        from Scripts.pipeline_core import Stable_Diffusion_Core as SD
        if not cls.pipeline_initialized:
            SD.pipeline_init(info.get("model"))
            cls.pipeline_initialized = True

        SD.pipe.to(info.get("device"))

        generator = SD.generator_seed(int(info.get("seed")), info.get("device"))

        #positive_prompts = SD.encode_prompts(SD.pipe, info.get("positive"))
        #negative_prompts = SD.encode_prompts(SD.pipe, info.get("negative"))

        compel = Compel(
            tokenizer=SD.pipe.tokenizer,
            text_encoder=SD.pipe.text_encoder
        )

        positive_prompts = compel(info.get("positive"))
        negative_prompts = compel(info.get("negative"))

        positive_embeds, negative_embeds = SD.pad_to_match(positive_prompts, negative_prompts)


        if info.get("scheduler") == "Karras":
            use_karras = True
        else:
            use_karras = False

        SD.sampler_define(SD.pipe, info.get("sampler"), use_karras)

        image = SD.image_generate(
            pipe=SD.pipe,
            pos_embeds=positive_embeds,
            neg_embeds=negative_embeds,
            generator=generator,
            steps=int(info.get("steps")),
            cfg=int(info.get("cfg")),
            width=int(info.get("width")),
            height=int(info.get("height")),
        )

        image.save

        return image