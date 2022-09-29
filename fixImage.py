import os

def defryImage(path_to_defry="defry/defry.out", image_to_defry="img/appLogo.png"):
    """Images taken from .ipa use a propietary extension by Apple that makes images unusable for other viewers.
    More info here:
    https://iphonedev.wiki/index.php/CgBI_file_format

    The code found in ../defry is used to revert these changes. Original code is from this repository:
    https://github.com/esjeon/pngdefry
    """    
    os.system(f"{path_to_defry} -s _out {image_to_defry}")


if __name__ == '__main__':
    defryImage()