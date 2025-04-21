from django.shortcuts import render
from .form import UploadFileForm
from PIL import Image, ImageOps, ImageFilter
import os
from django.conf import settings
from datetime import datetime

def apply_filter(input_path, preset):
    name, ext = os.path.splitext(os.path.basename(input_path))
    timestamp = datetime.now().strftime('%Y%m%H%M%S')
    output_name = f"{name}_{preset}_{timestamp}.jpg"
    output_path = os.path.join(settings.MEDIA_ROOT, 'output', output_name)
    

    im = Image.open(input_path)

    if preset == 'gray':
        im = ImageOps.grayscale(im)
    elif preset == 'edge':
        im = im.convert("L").filter(ImageFilter.FIND_EDGES)
    elif preset == 'poster':
        im = ImageOps.posterize(im, 3)
    elif preset == 'solar':
        im = ImageOps.solarize(im, threshold=80)
    elif preset == 'blur':
        im = im.filter(ImageFilter.GaussianBlur(15))  
    elif preset == 'sepia':
        sepia = []
        r, g, b = (239, 224, 185)
        for i in range(255):
            sepia.extend((r * i // 255, g * i // 255, b * i // 255))
        im = im.convert("L")
        im.putpalette(sepia)
        im = im.convert("RGB")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path)
    return output_name # relative path for media serving

def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['myfilefield']
            preset = form.cleaned_data['preset']

            upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image_file.name)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)

            with open(upload_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)

            output_filename = apply_filter(upload_path, preset)
            return render(request, 'process.html', {'outputfilename': output_filename})
    else:
        form = UploadFileForm()

    return render(request, 'home.html', {'form': form})