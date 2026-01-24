import os

def defryImage(image_to_defry, path_to_defry_executable="defry/defry.out"):
    """Images taken from .ipa use a propietary extension by Apple that makes images unusable for other viewers.
    More info here:
    https://iphonedev.wiki/index.php/CgBI_file_format

    The code found in ../defry is used to revert these changes. Original code is from this repository:
    https://github.com/esjeon/pngdefry
    """    
    os.system(f"{path_to_defry_executable} -s _out {image_to_defry}")