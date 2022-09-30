import colorgram

def extract_colors(inputImage, colors_to_extract: int=4):
    """Generates a color palette from an image.

    Args:
        inputImage (str/Image): It can take either a filename/path (String) or a Image
    
    Return:
        colors (list[Color]): color palette extracted from the image
    """
    colors = colorgram.extract(inputImage, colors_to_extract)
    colors.sort(key=lambda c: c.hsl.h)
    return colors