import os
import logging

import qrcode
from colorgram import Color
from PIL import Image, ImageDraw
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


def generate_eyes_mask(img):
    """Custom QR eyes are not supported in the qrcode package, so this method is used
    to generate a mask used for creating custom QR eyes.

    Args:
        img (Image): QR to mask and get the eyes from

    Returns:
        Image: mask to use for the eyes of the QR
    """
    img_size = img.size[0]
    eye_size = 70  # default
    quiet_zone = 40  # default
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((40, 40, 110, 110), fill=255)
    draw.rectangle((img_size-110, 40, img_size-40, 110), fill=255)
    draw.rectangle((40, img_size-110, 110, img_size-40), fill=255)
    return mask

def generateQrImage(data: str, colors: list = [Color(0, 0, 0, 1), Color(255, 255, 255, 1)], errorCorrectionLevel=qrcode.constants.ERROR_CORRECT_H, embedded_image="res/pinchLogo.png", output_path="out/qr_output.png"):
    """Generate QR image

    Args:
        data (str): data to put in the QR
        colors (list): array of colors to use, if no colors are set, black and white are used
        errorCorrectionLevel (_type_, optional): _description_. Defaults to qrcode.constants.ERROR_CORRECT_H.
        embedded_image (str, optional): _description_. Defaults to "pinchLogo.png".
        output_path (str, optional): _description_. Defaults to "qr_output.png".
    """

    qr = qrcode.QRCode(error_correction=errorCorrectionLevel)
    qr.add_data(data)

    eyes_back_color = colors[2].rgb
    eyes_front_color = colors[0].rgb

    body_back_color = colors[2].rgb
    body_front_color = colors[0].rgb

    # Generate eyes
    qr_eyes_img = qr.make_image(
        image_factory=StyledPilImage,
        eye_drawer=RoundedModuleDrawer(radius_ratio=1.2),
        color_mask=SolidFillColorMask(
            back_color=eyes_back_color,
            front_color=eyes_front_color,
        ),
    )

    # TODO: Possible upgrade? Replace pinch "P" bg color to the one used as front color
    # For now abandoned because it needs to transform svg to png and it does not behave well
    # from cairosvg import svg2png
    # if (embedded_image == "pinchLogo.svg"):
    #   #00AB52

    # Main QR body
    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(
            back_color=body_back_color,
            front_color=body_front_color,
        ),
        embeded_image_path=embedded_image,
    )

    # Composite QR with eyes
    mask = generate_eyes_mask(qr_img)
    final_img = Image.composite(qr_eyes_img, qr_img, mask)

    try:
        exists_output_path = os.path.exists(output_path)
        if not exists_output_path:
            os.makedirs(output_path)
    except:
        output_path = "out"
        logging.debug(f"Could not create folders, saving it to {output_path}")
        

    final_img.save(f"{output_path}/qr.png")


if __name__ == '__main__':
    colors = [Color(44, 44, 55, 1), Color(244, 44, 55, 1)]
    generateQrImage(data="https://www.youtube.com/watch?v=dQw4w9WgXcQ", colors=colors)
