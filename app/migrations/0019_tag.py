from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0018_alter_user_cover_alter_user_profile_pic"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("name_tag", models.TextField(blank=True, max_length=50)),
            ],
        ),
    ]
