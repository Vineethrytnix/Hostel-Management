# Generated by Django 4.1.2 on 2024-02-10 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_rooms_no_of_adults_rooms_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='image',
            field=models.FileField(default='event_image', upload_to='event_images/'),
        ),
    ]
