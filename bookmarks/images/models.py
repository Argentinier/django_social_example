from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from django.utils.text import slugify


class TimestampsMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Image(TimestampsMixin):
    user = models.ForeignKey(to=get_user_model(), related_name='images_created', on_delete=models.CASCADE)
    users_like = models.ManyToManyField(to=get_user_model(), related_name='images_liked', blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)

    @property
    def sort_desc(self):
        return truncatewords(self.description, 30)

    @property
    def likes(self):
        return self.users_like.count

    def get_absolute_url(self):
        return reverse(f'images:detail', args=[self.id, self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(self, *args, **kwargs)
