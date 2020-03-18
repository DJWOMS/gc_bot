import os
import importlib

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
print(__import__('views', globals={"__name__": __name__}))
