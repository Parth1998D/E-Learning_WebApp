# Generated by Django 4.0.4 on 2022-08-12 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_passwordreset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='image',
            field=models.ImageField(blank=True, upload_to='myapp/images/'),
        ),
    ]
