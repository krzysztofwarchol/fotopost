from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="follower",
            name="follower",
        ),
        migrations.AddField(
            model_name="follower",
            name="follower",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="following",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RemoveField(
            model_name="like",
            name="liker",
        ),
        migrations.AddField(
            model_name="like",
            name="liker",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
