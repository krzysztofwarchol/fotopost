from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="savers",
            field=models.ManyToManyField(
                related_name="saved", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(
            name="Saved",
        ),
    ]
