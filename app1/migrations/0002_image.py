# Generated by Django 4.0.10 on 2023-11-11 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_img', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]