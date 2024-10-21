# Generated by Django 5.1.1 on 2024-10-16 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0003_remove_flashcard_answer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardcontent',
            name='card_side',
        ),
        migrations.AddField(
            model_name='cardcontent',
            name='flashcard',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='sides', to='decks.flashcard'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cardcontent',
            name='side',
            field=models.CharField(choices=[('front', 'Front'), ('back', 'Back')], default=1, max_length=5),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CardSide',
        ),
    ]