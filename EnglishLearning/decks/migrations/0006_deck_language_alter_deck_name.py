# Generated by Django 5.1.1 on 2024-11-16 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0005_alter_deck_deck_image_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='language',
            field=models.CharField(blank=True, default='english', max_length=20),
        ),
        migrations.AlterField(
            model_name='deck',
            name='name',
            field=models.CharField(default='New Deck', max_length=200),
        ),
    ]
