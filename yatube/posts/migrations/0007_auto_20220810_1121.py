# Generated by Django 2.2.9 on 2022-08-10 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20220810_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET('Категория удалена'), related_name='+', to='posts.Group'),
        ),
    ]