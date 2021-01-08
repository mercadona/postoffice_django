import django.core.serializers.json
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postoffice_django', '0002_add_bulk_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishingerror',
            name='payload',
            field=django.db.models.JSONField(
                encoder=django.core.serializers.json.DjangoJSONEncoder),
        ),
        migrations.AlterField(
            model_name='publishingerror',
            name='attributes',
            field=django.db.models.JSONField(
                encoder=django.core.serializers.json.DjangoJSONEncoder,
                null=True
            ),
        ),
    ]
