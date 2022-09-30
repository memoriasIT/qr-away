from asyncore import write
from PIL import Image, ImageDraw, ImageFont

def pasteOnTop(im1, im2):
    w = max(im1.size[0], im2.size[0])
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (0, 0))

    return im

def writeCenteredTitle(text: str):
    font_path = 'font/RobotoCondensed-Bold.ttf'
    selected_size = 1
    for size in range(1, 150):
        font = ImageFont.FreeTypeFont(font_path, size=size)
        left, top, right, bottom = font.getbbox(text)
        w = right - left
        h = bottom - top
        
        if w > (final_img.width*0.5) or size > 54:
            break
            
        selected_size = size

    font = ImageFont.FreeTypeFont(font_path, size=selected_size)
    draw = ImageDraw.Draw(final_img)
    draw.text((final_img.width//2, 650), text, fill='black', anchor='mm', font=font)

def writeCenteredSubtitle(text: str):
    font_path = 'font/Roboto-Light.ttf'
    selected_size = 1
    for size in range(1, 150):
        font = ImageFont.FreeTypeFont(font_path, size=size)
        left, top, right, bottom = font.getbbox(text)
        w = right - left
        h = bottom - top
        
        if w > (final_img.width*0.5) or size > 40:
            break
            
        selected_size = size

    font = ImageFont.FreeTypeFont(font_path, size=selected_size)
    draw = ImageDraw.Draw(final_img)
    draw.text((final_img.width//2, 720), text, fill='black', anchor='mm', font=font)


img = Image.open("out/qr.png")
card_mask = Image.open("card_mask.png")

# Paste qr on top and mask out to have rounded corners
final_img = pasteOnTop(card_mask, img)
final_img = Image.composite(final_img, card_mask, card_mask)

text = "VERY T"
version = "v2.0.3"
writeCenteredTitle(text)
writeCenteredSubtitle(version)

# draw text in center of rectangle 200x100        



final_img.show("test.png")