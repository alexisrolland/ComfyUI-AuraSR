import numpy as np
import torch
from aura_sr import AuraSR
from PIL import Image


class downloadAuraSR:
    """Node to download AuraSR model."""

    # Node setup for ComfyUI
    CATEGORY = "AuraSR"
    FUNCTION = "execute"
    OUTPUT_NODE = False
    RETURN_TYPES = ("AURASR_MODEL",)

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "model": (
                    ['fal-ai/AuraSR', 'fal/AuraSR-v2'],
                    { "default": 'fal-ai/AuraSR'}
                ),
            }
        }

    def execute(self, model):
        MODEL = AuraSR.from_pretrained(model_id=model)
        return (MODEL,)

class RunAuraSR:
    """Node to run AuraSR model."""

    # Node setup for ComfyUI
    CATEGORY = "AuraSR"
    FUNCTION = "execute"
    OUTPUT_NODE = False
    RETURN_TYPES = ("IMAGE",)

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "AURASR_MODEL": ("AURASR_MODEL",),
                "IMAGE": ("IMAGE",),
                "avoid_seams": ("BOOLEAN", {"default": True}),
            }
        }

    def tensor2pil(self, image):
        batch_count = image.size(0) if len(image.shape) > 3 else 1
        if batch_count > 1:
            out = []
            for i in range(batch_count):
                out.extend(self.tensor2pil(image[i]))
            return out
        return [Image.fromarray(np.clip(255.0 * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))]

    def pil2tensor(self, image):
        if isinstance(image, list):
            return torch.cat([self.pil2tensor(img) for img in image], dim=0)
        return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

    def execute(self, AURASR_MODEL, IMAGE, avoid_seams):
        # Convert tensor to PIL image
        images = self.tensor2pil(IMAGE)

        # Check version of AuraSR model and upscale images
        upscaled_images = list()
        if avoid_seams:
            for image in images:
                upscaled_images.append(AURASR_MODEL.upscale_4x_overlapped(image))
        else:
            for image in images:
                upscaled_images.append(AURASR_MODEL.upscale_4x(image))

        # Convert PIL images to tensor
        upscaled_images = self.pil2tensor(upscaled_images)

        return (upscaled_images,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "downloadAuraSR": downloadAuraSR,
    "RunAuraSR": RunAuraSR
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "downloadAuraSR": "Download AuraSR",
    "RunAuraSR": "Run AuraSR"
}