# Generated by Django 2.2 on 2019-09-05 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_ingredient'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredient',
            new_name='Attribute',
        ),
    ]