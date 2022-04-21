from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from images.forms import ImageCreateForm
from images.models import Image


@login_required
def image_create(request):
    form = ImageCreateForm(request.GET)

    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, message=f'Image {new_item.title} was saved successfully!')

            return redirect(new_item.get_absolute_url())

    return render(
        request=request,
        template_name='images/image/create.html',
        context={
            'form': form,
            'section': 'images'
        })


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(
        request=request,
        template_name='images/image/detail.html',
        context={
            'image': image,
            'section': 'images'
        })