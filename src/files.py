import os
from typing import Optional

import pygame as pg
import yaml
from yaml import Loader


def load_resources_dir(directory, color_key=(255, 0, 255)):
    graphics = {}
    for res in os.listdir(directory):
        name, ext = os.path.splitext(res)
        if ext.lower() in [".png", ".jpg"]:
            img = pg.image.load(os.path.join(directory, res))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(color_key)
            if "white" in name or "black" in name:
                img = pg.transform.scale(img, (80, 80))
            graphics[name] = img
        elif ext.lower() == ".ttf":
            graphics[name] = pg.font.Font(os.path.join(directory, res), 30)  # Temp
    return graphics


def load_yaml(file_name: str):
    directory = os.path.join("resources", file_name)
    with open(directory) as file:
        return yaml.load(file, Loader)


def resources_from_dir(directories: list[str]):
    base_path = os.path.join("resources")

    _resources = {}
    for directory in directories:
        path = os.path.join(base_path, directory)
        _resources[directory] = load_resources_dir(path)
    return _resources
