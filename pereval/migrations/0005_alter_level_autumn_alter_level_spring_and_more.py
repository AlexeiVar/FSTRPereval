# Generated by Django 5.1.1 on 2024-10-07 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0004_remove_perevalimages_pereval_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='autumn',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='level',
            name='spring',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='level',
            name='summer',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='level',
            name='winter',
            field=models.CharField(blank=True, max_length=2),
        ),
    ]
