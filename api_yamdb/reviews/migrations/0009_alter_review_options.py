# Generated by Django 3.2 on 2024-12-27 00:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_alter_review_score'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
    ]
