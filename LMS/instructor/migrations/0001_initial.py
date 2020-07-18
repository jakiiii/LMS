# Generated by Django 2.2 on 2020-07-17 11:59

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lms.utils_file


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanySettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=250)),
                ('company_address', models.TextField()),
                ('company_email', models.CharField(max_length=32)),
                ('vat_registration_number', models.PositiveIntegerField()),
                ('vat_percentage', models.IntegerField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=50)),
                ('designation', models.CharField(blank=True, max_length=50, null=True)),
                ('commission', models.PositiveIntegerField(blank=True, null=True)),
                ('short_bio', models.TextField(blank=True, max_length=400, null=True)),
                ('long_bio', ckeditor.fields.RichTextField()),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('address_office', models.CharField(blank=True, max_length=250, null=True)),
                ('email', models.CharField(max_length=40)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('school', models.CharField(blank=True, max_length=250, null=True)),
                ('college', models.CharField(blank=True, max_length=250, null=True)),
                ('university', models.CharField(blank=True, max_length=250, null=True)),
                ('phd', models.CharField(blank=True, max_length=250, null=True)),
                ('image', models.ImageField(default='assets/images/instructor.png', upload_to=lms.utils_file.upload_image_path)),
                ('password', models.CharField(blank=True, max_length=32, null=True)),
                ('facebook', models.CharField(blank=True, max_length=150, null=True)),
                ('twitter', models.CharField(blank=True, max_length=150, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=150, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('language', models.ManyToManyField(blank=True, to='instructor.Language')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('experience_description', models.TextField(blank=True, max_length=500, null=True)),
                ('ex_period', models.DateField(blank=True, null=True)),
                ('ex_end_period', models.DateField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.Instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('Institute_name', models.CharField(blank=True, max_length=250, null=True)),
                ('from_date', models.DateField(blank=True, null=True)),
                ('to_date', models.DateField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.Instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('certification_description', models.TextField(blank=True, max_length=500, null=True)),
                ('period', models.DateField(blank=True, null=True)),
                ('ex_end_period', models.DateField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.Instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Awards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('award_description', models.TextField(blank=True, max_length=500, null=True)),
                ('ex_period', models.DateField(blank=True, null=True)),
                ('ex_end_period', models.DateField(blank=True, null=True)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instructor.Instructor')),
            ],
        ),
    ]
