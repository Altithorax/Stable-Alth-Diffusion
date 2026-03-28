
from diffusers import (
    StableDiffusionPipeline,
    DPMSolverSDEScheduler,
    DPMSolverMultistepScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    DDIMScheduler,
    LMSDiscreteScheduler,
    HeunDiscreteScheduler,
    UniPCMultistepScheduler
)
import torch
import PIL

class Stable_Diffusion_Core:
    pipe = None
    current_model = None

    @classmethod
    def pipeline_init(cls, model_path: str) -> StableDiffusionPipeline:
        if cls.pipe is None or cls.current_model != model_path:

            if cls.pipe is not None or cls.current_model != model_path:
                del cls.pipe
                torch.cuda.empty_cache()

            cls.pipe = StableDiffusionPipeline.from_single_file(
                model_path,
                torch_dtype=torch.float16,
                safety_checker=None
            )

            cls.current_model = model_path

        return cls.pipe
    
    @staticmethod
    def generator_seed(seed, device) -> torch.Tensor:
        
        generator = torch.Generator(device).manual_seed(seed)

        return generator
    
    def encode_prompts(pipe: StableDiffusionPipeline, prompt: str) -> torch.Tensor:

        tokenizer = pipe.tokenizer
        text_encoder = pipe.text_encoder

        max_length = tokenizer.model_max_length
        chunk_size = max_length - 2

        tokens = tokenizer(
            prompt,
            return_tensors="pt",
            add_special_tokens=False
        ).input_ids[0]

        if len(tokens) == 0:
            text_input = tokenizer(
                "",
                padding="max_length",
                max_length=max_length,
                return_tensors="pt"
            )

            with torch.no_grad():
                embeds = text_encoder(
                    text_input.input_ids.to(pipe.device)
                )[0]

            return embeds
        
        chunks = []

        for i in range(0, len(tokens), chunk_size):

            chunk = tokens[i:i + chunk_size]

            chunk = torch.cat([
                torch.tensor([tokenizer.bos_token_id]),
                chunk,
                torch.tensor([tokenizer.eos_token_id])
            ])

            chunk = chunk.unsqueeze(0).to(pipe.device)

            with torch.no_grad():
                embedding = text_encoder(chunk)[0]

            chunks.append(embedding)

        return torch.cat(chunks, dim=1)
    
    @staticmethod
    def pad_to_match(a: torch.Tensor, b: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:

        max_len = max(a.shape[1], b.shape[1])

        def pad(x):
            if x.shape[1] < max_len:
                pad_size = max_len - x.shape[1]
                padding = torch.zeros(
                    (x.shape[0], pad_size, x.shape[2]),
                    device=x.device,
                    dtype=x.dtype
                )
                x = torch.cat([x, padding], dim=1)
            return x

        return pad(a), pad(b)
    
    @staticmethod
    def image_generate(pipe: StableDiffusionPipeline,
                       pos_embeds: torch.Tensor,
                       neg_embeds: torch.Tensor,
                       generator: torch.Generator,
                       steps: int,
                       cfg: int,
                       width: int,
                       height: int
        ) -> PIL.Image.Image:
        image = pipe(
            prompt_embeds=pos_embeds,
            negative_prompt_embeds=neg_embeds,
            generator=generator,
            guidance_scale=cfg,
            width=width,
            height=height,
            num_inference_steps=steps
        ).images[0]

        return image
    
    @staticmethod
    def sampler_define(pipe, sampler, karras):

        if sampler == "DPM++ 2M":
            # DPM++ 2M
            pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                pipe.scheduler.config,
                use_karras_sigmas = karras
        )
        elif sampler == "DPM++ SDE":
            #DPM++ SDE
            pipe.scheduler = DPMSolverSDEScheduler.from_config(
                pipe.scheduler.config,
                use_karras_sigmas = karras
        )
        elif sampler == "Euler":
            #Euler
            pipe.scheduler = EulerDiscreteScheduler.from_config(
                pipe.scheduler.config,
                use_karras_sigmas = karras
        )
        elif sampler == "Euler A":
            #Euler A
            pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(
                pipe.scheduler.config,
                use_karras_sigmas = karras
        )
        elif sampler == "DDIM":
            #DDIM
            pipe.scheduler = DDIMScheduler.from_config(
                pipe.scheduler.config,
                use_karras_sigmas = karras
        )
        elif sampler == "LMS":
            #LMS
            pipe.scheduler = LMSDiscreteScheduler.from_config(
                pipe.scheduler.config,
                use_karras_sigmas = karras
        )
        elif sampler == "Heun":
            #Heun
            pipe.scheduler = HeunDiscreteScheduler.from_config(
                pipe.scheduler.config,
                use_karras_sigmas = karras
        )
        elif sampler == "UniPC":
            #UniPC
            pipe.scheduler = UniPCMultistepScheduler.from_config(
                pipe.scheduler.config,
                use_karras_sigmas = karras
        )