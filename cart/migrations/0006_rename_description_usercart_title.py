# Generated by Django 5.0 on 2024-01-18 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_usercart_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercart',
            old_name='description',
            new_name='title',
        ),
    ]
