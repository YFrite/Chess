import os
import pygame as pg


def load_all_gfx(directory, color_key=(255, 0, 255), accept=(".png", ".jpg", ".bmp")):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(color_key)
            graphics[name] = img
    return graphics


def graphics_from_dir(directories: list[str]):
    base_path = os.path.join("resources", "graphics")

    _GFX = {}
    for directory in directories:
        path = os.path.join(base_path, directory)
        _GFX[directory] = load_all_gfx(path)
    return _GFX
