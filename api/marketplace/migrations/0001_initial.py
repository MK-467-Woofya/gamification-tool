# Generated by Django 5.1 on 2024-10-28 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name of marketplace item')),
                ('cost', models.IntegerField(default=0, verbose_name='Price in shop_points')),
                ('partner', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name of collaborator')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description of the item')),
                ('date_time_added', models.DateTimeField(auto_now_add=True, verbose_name='When ttem was added to the marketplace')),
                ('is_listed', models.BooleanField(default=False, verbose_name='Is item purchaseable?')),
                ('date_time_listed', models.DateTimeField(blank=True, null=True, verbose_name='Datetime when item was listed')),
                ('date_time_unlisted', models.DateTimeField(blank=True, null=True, verbose_name='Datetime when item became unlisted')),
                ('img_url', models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='URL of image')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name of marketplace item')),
                ('cost', models.IntegerField(default=0, verbose_name='Price in shop_points')),
                ('partner', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name of collaborator')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description of the item')),
                ('date_time_added', models.DateTimeField(auto_now_add=True, verbose_name='When ttem was added to the marketplace')),
                ('is_listed', models.BooleanField(default=False, verbose_name='Is item purchaseable?')),
                ('date_time_listed', models.DateTimeField(blank=True, null=True, verbose_name='Datetime when item was listed')),
                ('date_time_unlisted', models.DateTimeField(blank=True, null=True, verbose_name='Datetime when item became unlisted')),
                ('text', models.CharField(blank=True, max_length=50, null=True, verbose_name='Title text')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
