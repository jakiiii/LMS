# Generated by Django 2.2 on 2020-07-17 11:59

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import lms.utils_file


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('cover_image', models.FileField(default='assets/default_images/no-image.png', upload_to=lms.utils_file.upload_image_path)),
                ('video', models.URLField(blank=True, max_length=300, null=True)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('tags', models.ManyToManyField(blank=True, to='blog.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
