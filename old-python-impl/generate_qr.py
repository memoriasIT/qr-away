import os
import qrcode
from PIL import Image, ImageDraw
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer

# Helper class to match your usage pattern if you don't have one defined
class Color:
    def __init__(self, r, g, b):
        self.rgb = (r, g, b)

def generate_eyes_mask(img, qr_version, box_size, border):
    """
    Dynamically generates a mask for the QR eyes (finder patterns).
    Standard QR eyes are always 7x7 modules.
    """
    width, height = img.size
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # Calculate pixel metrics
    eye_module_count = 7
    eye_size_px = eye_module_count * box_size
    border_px = border * box_size

    # Top Left Eye
    draw.rectangle(
        (border_px, border_px, border_px + eye_size_px, border_px + eye_size_px), 
        fill=255
    )

    # Top Right Eye
    tr_x = width - border_px - eye_size_px
    draw.rectangle(
        (tr_x, border_px, tr_x + eye_size_px, border_px + eye_size_px), 
        fill=255
    )

    # Bottom Left Eye
    bl_y = height - border_px - eye_size_px
    draw.rectangle(
        (border_px, bl_y, border_px + eye_size_px, bl_y + eye_size_px), 
        fill=255
    )

    return mask

def generateQrImage(
    data: str, 
    colors: list, 
    target_size: tuple = (500, 500),
    errorCorrectionLevel=qrcode.constants.ERROR_CORRECT_H, 
    embedded_image="res/pinchLogo.png", 
    output_path="out"
):
    """
    Generate a styled QR image at high quality without resizing/stretching.
    """
    
    # 1. Setup QR Data (First Pass)
    # We initialize with a dummy box_size to calculate the matrix dimensions
    qr = qrcode.QRCode(
        version=None, 
        error_correction=errorCorrectionLevel,
        box_size=1, 
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    # 2. Calculate Dynamic Box Size
    # We need to find the integer box_size that fits closest to target_size
    # Formula: Total Pixels = (Modules + 2*Border) * BoxSize
    matrix_size = qr.modules_count
    total_modules = matrix_size + (qr.border * 2)
    
    # Calculate how many pixels per module we can afford
    suggested_box_size = target_size[0] // total_modules
    
    # Ensure we don't go below 1 pixel per module
    if suggested_box_size < 1:
        suggested_box_size = 1
        
    # Update the QR object with the high-res box size
    qr.box_size = suggested_box_size
    
    print(f"Calculated Box Size: {qr.box_size}px (Total modules: {total_modules})")

    # 3. Parse Colors
    body_front = colors[0].rgb
    bg_color = colors[1].rgb if len(colors) > 1 else (255, 255, 255)
    eyes_front = colors[2].rgb if len(colors) > 2 else body_front

    # 4. Generate Image for the EYES (Square)
    qr_eyes_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=SquareModuleDrawer(),
        color_mask=SolidFillColorMask(
            back_color=bg_color,
            front_color=eyes_front,
        ),
    )

    # 5. Generate Image for the BODY (Rounded)
    embed_arg = embedded_image if os.path.exists(embedded_image) else None
    
    qr_body_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(
            back_color=bg_color,
            front_color=body_front,
        ),
        embeded_image_path=embed_arg
    )

    # 6. Composite Images using Mask
    mask = generate_eyes_mask(qr_body_img, qr.version, qr.box_size, qr.border)
    
    qr_eyes_img = qr_eyes_img.convert("RGBA")
    qr_body_img = qr_body_img.convert("RGBA")
    
    final_img = Image.composite(qr_eyes_img, qr_body_img, mask)

    # 7. Final Fit (Padding instead of Resizing)
    # Since box_size must be an integer, the generated QR might be slightly 
    # smaller than target_size (e.g. 790px vs 800px).
    # We paste it onto a background canvas to match target_size exactly without blur.
    
    if final_img.size != target_size:
        print(f"Native QR size is {final_img.size}. Centering on {target_size} canvas.")
        bg_canvas = Image.new("RGBA", target_size, bg_color)
        
        # Calculate center position
        offset_x = (target_size[0] - final_img.size[0]) // 2
        offset_y = (target_size[1] - final_img.size[1]) // 2
        
        bg_canvas.paste(final_img, (offset_x, offset_y), final_img)
        final_img = bg_canvas

    # 8. Save File
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    save_loc = os.path.join(output_path, "qr_output.png")
    final_img.save(save_loc)
    print(f"High Quality QR Code saved to: {save_loc}")

if __name__ == '__main__':
    # Example Usage
    my_colors = [
        Color(44, 44, 55),    # Dark Grey (Body)
        Color(255, 255, 255), # White (Background)
        Color(244, 44, 55)    # Red (Eyes)
    ]
    
    generateQrImage(
        data="https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
        colors=my_colors,
        target_size=(1000, 1000) # Output will be exactly 1000x1000 px, high quality
    )
