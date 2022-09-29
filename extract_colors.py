import colorgram

def extract_colors(inputImage):
    """Generates a color palette from an image.

    Args:
        inputImage (str/Image): It can take either a filename/path (String) or a Image
    """
    colors = colorgram.extract(inputImage, 6)
    colors.sort(key=lambda c: c.hsl.h)