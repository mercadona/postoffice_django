from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postoffice_django', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publishingerror',
            name='bulk',
            field=models.BooleanField(default=False),
        ),
    ]
