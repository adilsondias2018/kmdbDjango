# Generated by Django 3.2.7 on 2021-09-17 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appKMDb', '0004_alter_genre_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='synopsis',
            field=models.CharField(max_length=500),
        ),
    ]
