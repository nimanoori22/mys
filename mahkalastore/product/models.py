from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
# Create your models here.

class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children') 
    name = models.CharField(max_length=50, unique=True)
    keywords = models.CharField(max_length=150)
    slug = models.SlugField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' / '.join(full_path[::-1])

    
class Product(models.Model):

    STATUS = (
        (0, 'ناموجود'),
        (1, 'موجود'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=250)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=9, decimal_places=0)
    amount = models.IntegerField()
    slug = models.SlugField(null=False, unique=True)
    status = models.IntegerField(choices=STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    Image = models.ImageField(blank=True, upload_to='images/')
    
    def __str__(self):
        return self.name

    