# Generated by Django 2.2.19 on 2022-08-09 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20220809_0702'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='text_post',
            new_name='text',
        ),
    ]