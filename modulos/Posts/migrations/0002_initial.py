# Generated by Django 5.1 on 2025-02-03 17:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Categories", "0001_initial"),
        ("Posts", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Autor",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="Categories.category",
                verbose_name="Categoria",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="favorites",
            field=models.ManyToManyField(
                related_name="favorite_posts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Favoritos",
            ),
        ),
        migrations.AddField(
            model_name="log",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Posts.post"
            ),
        ),
        migrations.AddField(
            model_name="destacado",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="Posts.post"
            ),
        ),
        migrations.AddField(
            model_name="version",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Autor",
            ),
        ),
        migrations.AddField(
            model_name="version",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="Categories.category",
                verbose_name="Categoria",
            ),
        ),
    ]
