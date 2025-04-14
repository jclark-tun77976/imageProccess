from django import forms

class UploadFileForm(forms.Form):
    myfilefield = forms.ImageField()
    preset = forms.ChoiceField(choices=[
        ('gray', 'Grayscale'),
        ('edge', 'Edge Detection'),
        ('poster', 'Posterize'),
        ('solar', 'Solarize'),
        ('blur', 'Blur'),
        ('sepia', 'Sepia'),
    ])