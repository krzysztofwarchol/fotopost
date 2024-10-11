from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0015"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="bio",
            field=models.TextField(blank=True, max_length=160, null=True),
        ),
    ]
