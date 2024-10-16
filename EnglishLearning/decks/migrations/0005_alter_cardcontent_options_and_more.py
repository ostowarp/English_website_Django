# Generated by Django 5.1.1 on 2024-10-16 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0004_remove_cardcontent_card_side_cardcontent_flashcard_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cardcontent',
            options={},
        ),
        migrations.AlterField(
            model_name='cardcontent',
            name='content_type',
            field=models.CharField(choices=[('title', 'title'), ('text', 'Text'), ('image', 'Image')], max_length=5),
        ),
        migrations.AlterField(
            model_name='cardcontent',
            name='order',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]
