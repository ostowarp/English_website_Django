# Generated by Django 5.1.1 on 2024-11-22 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0010_deck_back_deck_front_deck_image_deckimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deckimage',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='deckimage',
            name='image',
            field=models.ImageField(upload_to='deck_images/'),
        ),
    ]
