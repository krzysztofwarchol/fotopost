from django.db import migrations, models


def add_classes(apps, schema_editor):

    classes = [
        "house",
        "birds",
        "sun",
        "valley",
        "nighttime",
        "boats",
        "mountain",
        "tree",
        "snow",
        "beach",
        "vehicle",
        "rocks",
        "reflection",
        "sunset",
        "road",
        "flowers",
        "ocean",
        "lake",
        "window",
        "plants",
        "buildings",
        "grass",
        "water",
        "animal",
        "person",
        "clouds",
        "sky",
        "Not detected",
    ]

    Tag = apps.get_model("app", "Tag")
    for class_ in classes:
        tag = Tag.objects.create(name_tag=class_)
        tag.save()


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0019_tag"),
    ]

    operations = [migrations.RunPython(add_classes)]
