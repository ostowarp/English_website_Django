# Generated by Django 5.1.1 on 2024-10-27 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
