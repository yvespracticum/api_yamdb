# Generated by Django 3.2 on 2024-12-05 23:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0003_auto_20241205_0103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='created',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='title',
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('score', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review'),
            preserve_default=False,
        ),
    ]
