# Generated by Django 5.1.1 on 2024-11-22 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0008_delete_cardcontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='back',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='flashcard',
            name='front',
            field=models.TextField(blank=True, null=True),
        ),
    ]
