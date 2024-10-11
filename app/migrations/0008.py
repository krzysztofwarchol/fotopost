from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="follower",
            name="follower",
        ),
        migrations.AddField(
            model_name="follower",
            name="follower",
            field=models.ManyToManyField(
                related_name="following", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
