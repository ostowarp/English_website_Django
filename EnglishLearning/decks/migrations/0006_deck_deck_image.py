# Generated by Django 5.1.1 on 2024-10-16 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0005_alter_cardcontent_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='deck_image',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to=''),
        ),
    ]