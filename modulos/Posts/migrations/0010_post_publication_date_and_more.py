# Generated by Django 5.1 on 2024-09-24 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Posts", "0009_alter_post_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="publication_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Fecha de publicacion"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="scheduled_publication_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Fecha de publicacion agendada"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="status",
            field=models.CharField(
                choices=[
                    ("Borrador", "Borrador"),
                    ("Esperando revision", "Esperando revision"),
                    ("Esperando publicacion", "Esperando publicacion"),
                    ("Publicado", "Publicado"),
                    ("INACTIVE", "INACTIVE"),
                ],
                default="Borrador",
                max_length=30,
                verbose_name="Status",
            ),
        ),
    ]
