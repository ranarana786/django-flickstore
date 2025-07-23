from django.db import models
from django.urls import reverse

# Category model

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(max_length=500, blank=True)
    cate_image = models.ImageField(upload_to="photos/categories", blank=True)

    def get_url(self):
        return reverse('category-link', args=[self.category_name])

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name

