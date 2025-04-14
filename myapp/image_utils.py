from PIL import Image, ImageOps, ImageFilter
import os

def apply_filter(input_path, preset):
    im = Image.open(input_path)
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    output_path = f"media/processed/{name}_out.jpg"

    if preset == 'gray':
        im = ImageOps.grayscale(im)
    elif preset == 'edge':
        im = im.convert("L").filter(ImageFilter.FIND_EDGES)
    elif preset == 'poster':
        im = ImageOps.posterize(im, 3)
    elif preset == 'solar':
        im = ImageOps.solarize(im, threshold=80)
    elif preset == 'blur':
        im = im.filter(ImageFilter.BLUR)
    elif preset == 'sepia':
        sepia = []
        r, g, b = (239, 224, 185)
        for i in range(255):
            sepia.extend((r*i/255, g*i/255, b*i/255))
        im = im.convert("L")
        im.putpalette(sepia)
        im = im.convert("RGB")

    im.save(output_path)
    return output_path.replace('media/', '')  # Relative path for static serving