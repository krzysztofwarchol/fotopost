from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="likes_count",
        ),
        migrations.AddField(
            model_name="post",
            name="likers",
            field=models.ManyToManyField(
                related_name="likes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(
            name="Like",
        ),
    ]
