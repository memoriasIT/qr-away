import os
from PIL import Image
from generate_qr import generateQrImage
from generate_card import generateCardFromQr
from colorgram import Color
from app_platform import AppPlatform

# Define high-contrast colors (Gold background, Midnight Blue foreground)
colors = [
    Color(0, 27, 72, 0),    # #001B48 (Front Color)
    Color(0, 27, 72, 0),    
    Color(244, 199, 1, 0),  # #F4C701 (Back Color)
    Color(244, 199, 1, 0),  
]

def process_platform(url, platform, name, version, output_dir):
    """Generates the QR and Card for a specific platform."""
    if not url.strip():
        return None

    # Setup paths
    platform_label = platform.name.lower()
    qr_out = os.path.join(output_dir, f"qr_{platform_label}.png")
    card_out = os.path.join(output_dir, f"card_{platform_label}.png")

    # 1. Generate QR Image
    generateQrImage(
        data=url, 
        colors=colors, 
        output_path=output_dir, 
        embedded_image="res/logo.png"
    )
    # The internal generateQrImage likely saves to 'qr.png', 
    # so we rename it to avoid overwriting during the next loop
    temp_path = os.path.join(output_dir, "qr.png")
    if os.path.exists(temp_path):
        os.replace(temp_path, qr_out)

    # 2. Generate Card Image
    generateCardFromQr(
        app_name=name,
        app_platform=platform,
        app_version=version,
        qr_path=qr_out,
        output_path=card_out,
    )
    return card_out

def main():
    # User Inputs
    android_url = input("Enter Android release URL (leave empty to skip): ")
    ios_url = input("Enter iOS release URL (leave empty to skip): ")

    if not android_url.strip() and not ios_url.strip():
        print("No URLs provided. Exiting.")
        return

    output_path = "out/manual"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    app_name = "BNR Dev"
    app_version = "7.1.0"

    # Generate individual cards
    android_card = process_platform(android_url, AppPlatform.ANDROID, app_name, app_version, output_path)
    ios_card = process_platform(ios_url, AppPlatform.IOS, app_name, app_version, output_path)

    # Logic to join images
    generated_cards = [path for path in [android_card, ios_card] if path and os.path.exists(path)]

    if len(generated_cards) == 2:
        # Join side by side
        img1 = Image.open(generated_cards[0])
        img2 = Image.open(generated_cards[1])

        # Calculate combined dimensions
        total_width = img1.width + img2.width + 40 # 40px padding
        max_height = max(img1.height, img2.height)

        combined_img = Image.new('RGBA', (total_width, max_height), (255, 255, 255, 0))
        combined_img.paste(img1, (0, 0))
        combined_img.paste(img2, (img1.width + 40, 0))

        final_path = os.path.join(output_path, "combined_platforms.png")
        combined_img.save(final_path)
        print(f"Success! Combined image saved at: {final_path}")
    
    elif len(generated_cards) == 1:
        print(f"Single platform generated: {generated_cards[0]}")

if __name__ == "__main__":
    main()
