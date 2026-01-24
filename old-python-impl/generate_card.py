from PIL import Image, ImageDraw, ImageFont, ImageChops
try:
    from app_platform import AppPlatform
except ImportError:
    # Placeholder if module is missing during generation
    pass

def pasteOnTop(im1, im2):
    w = max(im1.size[0], im2.size[0])
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (0, 0))

    return im

def writeCenteredTitle(text: str, background_image: Image):
    font_path = 'res/font/RobotoCondensed-Bold.ttf'
    selected_size = 1
    for size in range(1, 150):
        font = ImageFont.FreeTypeFont(font_path, size=size)
        left, top, right, bottom = font.getbbox(text)
        w = right - left
        h = bottom - top
        
        if w > (background_image.width*0.5) or size > 54:
            break
            
        selected_size = size

    font = ImageFont.FreeTypeFont(font_path, size=selected_size)
    draw = ImageDraw.Draw(background_image)
    draw.text((background_image.width//2, 650), text, fill='black', anchor='mm', font=font)

def writeCenteredSubtitle(text, background_image: Image):
    font_path = 'res/font/Roboto-Light.ttf'
    selected_size = 1
    for size in range(1, 150):
        font = ImageFont.FreeTypeFont(font_path, size=size)
        left, top, right, bottom = font.getbbox(text)
        w = right - left
        h = bottom - top
        
        if w > (background_image.width*0.5) or size > 40:
            break
            
        selected_size = size

    font = ImageFont.FreeTypeFont(font_path, size=selected_size)
    draw = ImageDraw.Draw(background_image)
    draw.text((background_image.width//2, 710), text, fill='black', anchor='mm', font=font)

def pastePlatformIcon(platform: 'AppPlatform', background_image: Image):
    if platform == AppPlatform.ANDROID:
        platform_icon = Image.open("res/android-icon.png")
    elif platform == AppPlatform.IOS:
        platform_icon = Image.open("res/ios-icon.png")
    else:
        return

    platform_icon = platform_icon.resize((57, 57))
    background_image.paste(platform_icon, (background_image.width//2-30, 750), platform_icon)


def generateCardFromQr(app_name: str, app_platform: 'AppPlatform', app_version: str, qr_path: str, output_path: str):
    card_mask = Image.open("res/card_mask.png").convert("RGBA")  # The card, with transparency for corners
    qr_img = Image.open(qr_path).convert("RGBA")

    # Get card size for alignment
    card_w, card_h = card_mask.size

    # --- 1. Resize QR to fit the FULL WIDTH of the mask ---
    # Changed from fixed 650 to card_w to ensure it covers the width
    target_width = card_w
    
    # Calculate height based on aspect ratio to prevent distortion
    w_percent = (target_width / float(qr_img.size[0]))
    target_height = int((float(qr_img.size[1]) * float(w_percent)))
    
    qr_img = qr_img.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # --- 2. Masking the QR to the Card Shape ---
    # Create a transparent canvas for the QR
    qr_canvas = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    
    # Paste QR at the top-left (0, 0)
    qr_canvas.paste(qr_img, (0, 0))

    # Extract the alpha channel from the card mask (defines the shape/rounded corners)
    mask_alpha = card_mask.split()[3]
    
    # Multiply the QR's alpha by the Mask's alpha.
    # This cuts the QR code where the card is transparent (the corners)
    qr_canvas.putalpha(ImageChops.multiply(qr_canvas.split()[3], mask_alpha))

    # --- 3. Composite ---
    # Now composite the clipped QR onto the card background
    card_with_qr = Image.alpha_composite(card_mask, qr_canvas)

    # Draw texts and icon overlays
    writeCenteredTitle(app_name, card_with_qr)
    writeCenteredSubtitle(app_version, card_with_qr)
    try:
        pastePlatformIcon(app_platform, card_with_qr)
    except NameError:
        pass # Handle case where AppPlatform is not defined in this context

    # Save and show
    card_with_qr.save(output_path)
    card_with_qr.show()
