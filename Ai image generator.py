from diffusers import StableDiffusionPipeline
import torch

model_id = 'CompVis/stable-diffusion-v1-4'
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.to('cuda')

prompt = 'A futuristic city at sunset, cinematic lighting'
image = pipe(prompt).images[0]
image.save('generated_image.png')
