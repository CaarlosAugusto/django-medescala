# Generated by Django 3.2.5 on 2025-03-03 14:19

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=130)),
                ('endereco', models.CharField(max_length=250)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.EmailField(max_length=254, unique=True)),
                ('tipo', models.CharField(choices=[('medico', 'Médico'), ('paciente', 'Paciente')], max_length=10)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('groups', models.ManyToManyField(related_name='escala_app_users', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(related_name='escala_app_users_permissions', to='auth.Permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_nascimento', models.DateField()),
                ('endereco', models.CharField(max_length=255)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='paciente', to='escala_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crm', models.CharField(max_length=20, unique=True)),
                ('especialidade', models.CharField(max_length=100)),
                ('data_admissao', models.DateField()),
                ('status', models.BooleanField(default=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='medico', to='escala_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Integracao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_calendar_token', models.CharField(blank=True, max_length=255, null=True)),
                ('whatsapp_api_token', models.CharField(blank=True, max_length=255, null=True)),
                ('medico', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='integracoes', to='escala_app.medico')),
            ],
        ),
        migrations.CreateModel(
            name='HorarioDisponivel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(choices=[('segunda', 'Segunda-feira'), ('terca', 'Terça-feira'), ('quarta', 'Quarta-feira'), ('quinta', 'Quinta-feira'), ('sexta', 'Sexta-feira'), ('sabado', 'Sábado'), ('domingo', 'Domingo')], max_length=10)),
                ('hora_inicio', models.TimeField()),
                ('hora_fim', models.TimeField()),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios_disponiveis', to='escala_app.medico')),
            ],
        ),
        migrations.CreateModel(
            name='Assinatura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plano', models.CharField(choices=[('mensal', '$20/mês'), ('trimestral', '$50/trimestre'), ('anual', '$150/ano')], max_length=20)),
                ('data_inicio', models.DateField(auto_now_add=True)),
                ('data_expiracao', models.DateField()),
                ('status', models.BooleanField(default=True)),
                ('medico', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assinatura', to='escala_app.medico')),
            ],
        ),
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('hora', models.TimeField()),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('confirmado', 'Confirmado'), ('cancelado', 'Cancelado'), ('realizado', 'Realizado')], default='pendente', max_length=10)),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='escala_app.medico')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='escala_app.paciente')),
                ('posto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='escala_app.posto')),
            ],
        ),
    ]
