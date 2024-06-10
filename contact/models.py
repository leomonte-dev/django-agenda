from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# id (primary key)
# first_name (string), last_name (string), phone (string)
# email (email), created_date (date), description (text)
# category (foreign key), show (boolean), owner (foreign key)
# picture (image)

# class Contact(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     phone = models.CharField(max_length=20)
#     email = models.EmailField()
#     created_date = models.DateField()
#     description = models.TextField()
#     show = models.BooleanField()
#     picture = models.ImageField(upload_to='contacts')
#     category = models.ForeignKey('Category', on_delete=models.CASCADE)
#     owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.first_name

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    show = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='pictures/%Y/%m/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
