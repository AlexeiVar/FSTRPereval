# Generated by Django 5.1.1 on 2024-10-07 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0014_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pereval',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
