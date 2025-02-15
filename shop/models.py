from random import choice
from string import ascii_lowercase, digits

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def rand_slug():
    return ''.join(choice(ascii_lowercase + digits) for _ in range(3))


class Category(models.Model):
    """
    Represents a category in the shop, allowing hierarchical relationships.

    Attributes:
        name (CharField): The name of the category.
        parent (ForeignKey): A reference to the parent category, enabling nested categories.
        slug (SlugField): A unique URL-friendly identifier for the category.
        created_at (DateTimeField): The timestamp when the category was created.

    Meta:
        unique_together: Ensures that the combination of slug and parent is unique.
        verbose_name: The human-readable name for the model.
        verbose_name_plural: The plural form of the human-readable name.

    Methods:
        __str__(): Returns the full hierarchical path of the category.
        save(*args, **kwargs): Generates a slug if not provided and saves the category instance.
    """

    name = models.CharField('Category', max_length=250, db_index=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children', null=True, blank=True
    )
    slug = models.SlugField('URL', max_length=250, unique=True, null=False, editable=True)

    created_at = models.DateTimeField('Date', auto_now_add=True)

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        full_path = [self.name]
        k = self.parent

        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' > '.join(full_path[::-1])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' + self.name)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('category', kwargs={'pk': self.pk})


class Product(models.Model):
    """
    Represents a product in the shop.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField('Title', max_length=250)
    brand = models.CharField('Brand', max_length=250)
    description = models.TextField('Description', blank=True)
    slug = models.SlugField('URL', max_length=250)
    price = models.DecimalField('Price', max_digits=7, decimal_places=2, default=00.00)
    image = models.ImageField('Image', upload_to='products/products/%Y/%m/%d')
    available = models.BooleanField('Availability', default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse('model_detail', kwargs={'pk': self.pk})


class ProductManager(models.Manager):
    """
    Custom manager for the Product model that filters the queryset to include
    only available products.
    """

    def get_queryset(self):
        return super().get_queryset().filter(available=True)


class ProductProxy(Product):
    """
    A proxy model for the Product class that uses a custom manager to filter
    available products.
    """

    objects = ProductManager()

    class Meta:
        proxy = True