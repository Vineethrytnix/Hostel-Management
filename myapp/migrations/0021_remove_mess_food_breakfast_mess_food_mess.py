# Generated by Django 4.2.10 on 2024-02-21 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_fees_structure'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mess_food',
            name='breakfast',
        ),
        migrations.AddField(
            model_name='mess_food',
            name='mess',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
