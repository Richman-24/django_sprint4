# Generated by Django 5.0.6 on 2024-07-08 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_image_alter_post_location_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'default_related_name': 'posts', 'ordering': ['-pub_date'], 'verbose_name': 'публикация', 'verbose_name_plural': 'Публикации'},
        ),
    ]
