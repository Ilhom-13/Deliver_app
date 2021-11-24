# Generated by Django 3.2.9 on 2021-11-22 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import food.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to=food.models.custom_dir_path)),
                ('slug', models.SlugField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('quantity', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='food.category')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('open_at', models.TimeField()),
                ('close_at', models.TimeField()),
                ('day_off', models.CharField(choices=[('Mn', 'Monday'), ('Ts', 'Tuesday'), ('Wd', 'Wednesday'), ('Thr', 'Thursday'), ('Fr', 'Friday'), ('St', 'Saturday'), ('Sn', 'Sunday')], default='Sn', max_length=32)),
                ('contact', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress', models.CharField(max_length=250)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('done', 'completed'), ('delivering', 'on the way'), ('preparing', 'being cooked')], default='preparing', max_length=32)),
                ('items', models.ManyToManyField(related_name='orders', to='food.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.restaurant'),
        ),
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(choices=[('Tashkent', 'Tashkent'), ('Andijan', 'Andijan'), ('Namangan', 'Namangan'), ('Fergana', 'Fergana'), ('Karshi', 'Karshi'), ('Termiz', 'Termiz'), ('Nukus', 'Nukus'), ('Samarkand', 'Samarkand'), ('Navai', 'Navai'), ('Bukhara', 'Bukhara'), ('Khorezm', 'Khorezm'), ('Jizzakh', 'Jizzakh')], default='Tashkent', max_length=64)),
                ('district', models.CharField(max_length=250)),
                ('place', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='adress', to='food.restaurant')),
            ],
            options={
                'verbose_name_plural': 'Adresses',
            },
        ),
    ]
    