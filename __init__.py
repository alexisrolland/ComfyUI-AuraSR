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
                    ['fal-ai/AuraSR',],
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
            }
        }

    def execute(self, AURASR_MODEL, IMAGE,):
        # Convert tensor to PIL image
        image = Image.fromarray(np.clip(255. * IMAGE.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

        # Upscale
        upscaled_image = AURASR_MODEL.upscale_4x(image)

        # Convert PIL image to tensor
        tensor = torch.from_numpy(np.array(upscaled_image ).astype(np.float32) / 255.0).unsqueeze(0)
        return (tensor,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "downloadAuraSR": downloadAuraSR,
    "RunAuraSR": RunAuraSR,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "downloadAuraSR": "Download AuraSR",
    "RunAuraSR": "Run AuraSR",
}