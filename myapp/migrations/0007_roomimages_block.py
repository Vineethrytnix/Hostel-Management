# Generated by Django 4.2.10 on 2024-02-09 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_rooms_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomimages',
            name='block',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='myapp.blocks'),
        ),
    ]