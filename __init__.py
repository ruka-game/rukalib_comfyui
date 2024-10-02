from .nodes.prompt_enhancer import *
from .nodes.debug_probe import *

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "RukaPromptEnhancer": RukaPromptEnhancer,
    "RukaDebugProbe": RukaDebugProbe,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "RukaPromptEnhancer": "Ruka Prompt Enhancer 🌈",
    "RukaDebugProbe": "Ruka Debug Probe 🌈",
}

WEB_DIRECTORY = "./web"