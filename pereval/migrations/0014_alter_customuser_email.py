# Generated by Django 5.1.1 on 2024-10-07 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0013_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
