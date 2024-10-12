from . import nodes

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "LoadAuraSR": nodes.LoadAuraSR,
    "RunAuraSR": nodes.RunAuraSR
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadAuraSR": "DownLoad And Load AuraSR",
    "RunAuraSR": "Run AuraSR"
}