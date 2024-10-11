from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0020_tag_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="PostTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_tags",
                        to="app.post",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_tags",
                        to="app.tag",
                    ),
                ),
            ],
        ),
    ]
