# Generated by Django 3.2.7 on 2021-09-17 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appKMDb', '0003_rename_user_review_critic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='movie',
            field=models.ManyToManyField(related_name='genres', to='appKMDb.Movie'),
        ),
    ]
