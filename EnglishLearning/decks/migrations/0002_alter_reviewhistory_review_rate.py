# Generated by Django 5.1 on 2024-09-02 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewhistory',
            name='review_rate',
            field=models.CharField(choices=[('Easy Rate', 'Easy'), ('Good Rate', 'Good'), ('Hard Rate', 'Hard'), ('Again Rate', 'Again')], max_length=200),
        ),
    ]