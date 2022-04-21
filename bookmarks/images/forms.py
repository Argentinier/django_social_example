import tempfile
from pathlib import PurePosixPath

import requests
from django import forms
from django.core import files
from django.core.files.base import ContentFile
from django.utils.text import slugify

from images.models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description', 'url')

        # widgets = {
        #     'url': forms.HiddenInput,
        # }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ('.jpg', '.jpeg')
        extension = self.get_file_extension_from_url(url)

        if extension not in valid_extensions:
            raise forms.ValidationError(f'Image extension "{extension}" is not valid.'
                                        f'Allowed extensions: {", ".join(valid_extensions)}')

        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = self.get_file_extension_from_url(image_url)
        image_name = f'{name}{extension}'

        # Download the Image from the given URL
        response = requests.get(url=image_url, stream=True)

        # Save a temporary image (not on disk)
        temp = tempfile.NamedTemporaryFile(delete=True)

        # Write the streamed data into the temp file
        for block in response.iter_content(chunk_size=1024 * 8):
            temp.write(block)

        image.image.save(image_name, files.File(temp), save=False)

        if commit:
            image.save()

        return image

    @staticmethod
    def get_file_extension_from_url(url):
        return PurePosixPath(url).suffix.lower()
