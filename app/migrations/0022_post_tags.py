from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0021_posttag"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="tags", to="app.tag"),
        ),
    ]
