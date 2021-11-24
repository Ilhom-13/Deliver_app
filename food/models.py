from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Restaurant(models.Model):

    DAYS = (
        ('Mn', 'Monday'),
        ('Ts', 'Tuesday'),
        ('Wd', 'Wednesday'),
        ('Thr', 'Thursday'),
        ('Fr', 'Friday'),
        ('St', 'Saturday'),
        ('Sn', 'Sunday')
    )

    name = models.CharField(max_length=250, unique=True)
    open_at = models.TimeField()
    close_at = models.TimeField()
    day_off = models.CharField(max_length=32, choices=DAYS, default='Sn')
    contact = models.CharField(max_length=32)
    email = models.EmailField()
    slug = models.SlugField()

    def __str__(self):
        return self.name


def custom_dir_path(instance, filename):
    return f'{instance.__class__.__name__.lower()}/{filename}'


class Adress(models.Model):
    CITIES = (
        ('Tashkent', 'Tashkent'),
        ('Andijan', 'Andijan'),
        ('Namangan', 'Namangan'),
        ('Fergana', 'Fergana'),
        ('Karshi', 'Karshi'),
        ('Termiz', 'Termiz'),
        ('Nukus', 'Nukus'),
        ('Samarkand', 'Samarkand'),
        ('Navai', 'Navai'),
        ('Bukhara', 'Bukhara'),
        ('Khorezm', 'Khorezm'),
        ('Jizzakh', 'Jizzakh')
    )
    city = models.CharField(max_length=64, choices=CITIES, default='Tashkent')
    district = models.CharField(max_length=250)
    place = models.OneToOneField(Restaurant, null=True, related_name='adress', on_delete=models.SET_NULL)

    def __str__(self):
        return self.district

    class Meta:
        verbose_name_plural = 'Adresses'


class Item(models.Model):
    RATINGS = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to=custom_dir_path)
    slug = models.SlugField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATINGS, null=True, blank=True)
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    num_of_sold = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('food:item-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        size = (250, 250)
        img.thumbnail(size)
        img.save(self.image.path)


class Order(models.Model):
    ORDER_STATUS = (
        ('done', 'completed'),
        ('delivering', 'on the way'),
        ('preparing', 'being cooked')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='orders',)
    adress = models.CharField(max_length=250)
    phone = models.CharField(max_length=20, null=True, default=None)
    total_price = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, choices=ORDER_STATUS, default='preparing')

    def all_items(self):
        items = ''
        for item in self.items.all():
            items += f'{item.name} : {item.quantity} '
        return items

    def get_item_owner(self):
        return self.items.all().first().owner

    def __str__(self):
        return f'Order by {self.user.user_name}'
