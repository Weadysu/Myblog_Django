# Generated by Django 3.0.2 on 2020-02-01 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200201_0813'),
    ]

    operations = [
        migrations.RenameField(
            model_name='readnum',
            old_name='readed_num',
            new_name='read_num',
        ),
    ]
