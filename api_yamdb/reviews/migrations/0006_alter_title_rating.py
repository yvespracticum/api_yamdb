# Generated by Django 3.2 on 2024-12-09 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
