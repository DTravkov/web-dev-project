from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_pendingdiscipline_author'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingProfessor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_pending_professors', to=settings.AUTH_USER_MODEL)),
                ('discipline', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pending_professors', to='api.discipline')),
            ],
        ),
        migrations.AddConstraint(
            model_name='pendingprofessor',
            constraint=models.UniqueConstraint(fields=('name', 'surname', 'discipline'), name='unique_pending_professor_per_discipline'),
        ),
    ]
