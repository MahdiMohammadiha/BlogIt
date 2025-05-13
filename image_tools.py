from PIL import Image
import os


def merge_images_with_gap(
    img1_path: str,
    img2_path: str,
    output_path: str,
    gap_size: int,
    gap_color: str,
    direction: str,
) -> None:
    # Load images
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    # Resize images to same height or width if necessary
    if direction in ["left", "right"]:
        common_height = max(img1.height, img2.height)
        if img1.height != common_height:
            img1 = img1.resize((img1.width, common_height))
        if img2.height != common_height:
            img2 = img2.resize((img2.width, common_height))
    elif direction in ["up", "down"]:
        common_width = max(img1.width, img2.width)
        if img1.width != common_width:
            img1 = img1.resize((common_width, img1.height))
        if img2.width != common_width:
            img2 = img2.resize((common_width, img2.height))

    # Create gap
    if direction in ["left", "right"]:
        gap = Image.new("RGB", (gap_size, img1.height), gap_color)
    else:
        gap = Image.new("RGB", (img1.width, gap_size), gap_color)

    # Merge images
    if direction == "right":
        new_img = Image.new("RGB", (img1.width + gap_size + img2.width, img1.height))
        new_img.paste(img1, (0, 0))
        new_img.paste(gap, (img1.width, 0))
        new_img.paste(img2, (img1.width + gap_size, 0))
    elif direction == "left":
        new_img = Image.new("RGB", (img2.width + gap_size + img1.width, img1.height))
        new_img.paste(img2, (0, 0))
        new_img.paste(gap, (img2.width, 0))
        new_img.paste(img1, (img2.width + gap_size, 0))
    elif direction == "down":
        new_img = Image.new("RGB", (img1.width, img1.height + gap_size + img2.height))
        new_img.paste(img1, (0, 0))
        new_img.paste(gap, (0, img1.height))
        new_img.paste(img2, (0, img1.height + gap_size))
    elif direction == "up":
        new_img = Image.new("RGB", (img1.width, img2.height + gap_size + img1.height))
        new_img.paste(img2, (0, 0))
        new_img.paste(gap, (0, img2.height))
        new_img.paste(img1, (0, img2.height + gap_size))
    else:
        raise ValueError("Direction must be one of: up, down, left, right")

    # Save result
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    new_img.save(output_path)
    print(f"Image saved to {output_path}")


if __name__ == "__main__":
    pass
