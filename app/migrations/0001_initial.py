# Generated by Django 5.1.5 on 2025-01-27 16:52

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campo1', models.CharField(max_length=200, verbose_name='Campo 1')),
                ('campo2', models.CharField(max_length=200, verbose_name='Campo 2')),
                ('campo3', models.CharField(max_length=200, verbose_name='Campo 3')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
            ],
        ),
        migrations.CreateModel(
            name='Treino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_treino', models.CharField(choices=[('treino_funcional', 'Treino Funcional'), ('mobilidade', 'Mobilidade'), ('força', 'Força'), ('mobilidade', 'Mobilidade'), ('total_fit', 'Total FIT')], max_length=50)),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fim', models.TimeField()),
                ('dia_da_semana', models.CharField(choices=[('segunda-feira', 'Segunda-feira'), ('terça-feira', 'Terça-feira'), ('quarta-feira', 'Quarta-feira'), ('quinta-feira', 'Quinta-feira'), ('sexta-feira', 'Sexta-feira'), ('sábado', 'Sábado'), ('domingo', 'Domingo')], max_length=20)),
                ('dia_semana_num', models.IntegerField(blank=True, editable=False, null=True)),
                ('max_participantes', models.PositiveIntegerField(default=0)),
                ('max_lista_espera', models.PositiveIntegerField(default=0)),
                ('reservas_horas_antes', models.PositiveIntegerField(choices=[(1, '1 hora antes'), (6, '6 horas antes'), (12, '12 horas antes'), (24, '24 horas antes'), (48, '48 horas antes')], default=24)),
                ('reservas_horas_fecho', models.IntegerField(choices=[(0, 'No início do treino'), (1, '1 hora antes'), (2, '2 horas antes'), (6, '6 horas antes'), (12, '12 horas antes')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Utilizadores',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contacto', models.IntegerField()),
                ('data_nascimento', models.DateField()),
                ('genero', models.CharField(choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino')], max_length=12)),
                ('morada', models.CharField(blank=True, max_length=255, null=True)),
                ('codigo_postal', models.CharField(blank=True, max_length=8, null=True)),
                ('localidade', models.CharField(blank=True, max_length=100, null=True)),
                ('funcao', models.CharField(choices=[('Inativo', 'Inativo'), ('Ativo', 'Ativo')], default='Ativo', max_length=20)),
                ('nif', models.IntegerField()),
                ('pretende_recibo', models.CharField(choices=[('Sim', 'Sim'), ('Nao', 'Não')], max_length=3)),
                ('profissao', models.CharField(max_length=255)),
                ('classificacao_esforco_na_profissao', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('fumador', models.CharField(choices=[('Sim', 'Sim'), ('Nao', 'Não')], max_length=3)),
                ('problemas_saude', models.CharField(choices=[('Sim', 'Sim'), ('Nao', 'Não')], max_length=3)),
                ('limitacoes_para_pratica_exercicio_fisico', models.CharField(choices=[('Sim', 'Sim'), ('Nao', 'Não')], max_length=3)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='utilizadores_set', related_query_name='utilizadores', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='utilizadores_set', related_query_name='utilizadores', to='auth.permission')),
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
            name='Dados_biometricos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idade', models.CharField(blank=True, max_length=2, null=True)),
                ('altura', models.FloatField(blank=True, null=True)),
                ('peso', models.FloatField(blank=True, null=True)),
                ('imc', models.FloatField(blank=True, editable=False, null=True)),
                ('massa_gorda', models.CharField(blank=True, max_length=5, null=True)),
                ('massa_muscular', models.CharField(blank=True, max_length=4, null=True)),
                ('agua', models.CharField(blank=True, max_length=4, null=True)),
                ('gordura_visceral', models.CharField(blank=True, max_length=4, null=True)),
                ('idade_biologica', models.CharField(blank=True, max_length=2, null=True)),
                ('nivel_fisico', models.CharField(blank=True, max_length=50, null=True)),
                ('data_registo', models.DateField(auto_now_add=True)),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecordesNomes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recordes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('predefinidos', models.CharField(blank=True, choices=[('vazio', 'Escolhe uma opção'), ('peso_morto', 'Peso Morto'), ('agachamento_com_barra', 'Agachamento c/barra'), ('remada', 'Remada'), ('press_ombro', 'Press de Ombro'), ('flexoes', 'Flexões'), ('burpees', 'Burpees'), ('elevacao', 'Elevação'), ('agachamento_livre', 'Agachamento livre')], max_length=100, null=True)),
                ('valor', models.FloatField()),
                ('data_do_recorde', models.DateField()),
                ('data_criacao_recorde', models.DateField(auto_now_add=True)),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('nome', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.recordesnomes')),
            ],
        ),
        migrations.CreateModel(
            name='Reservas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmado', models.BooleanField(default=False)),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('treino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.treino')),
            ],
        ),
        migrations.CreateModel(
            name='ListaEspera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_entrada', models.DateTimeField(auto_now_add=True)),
                ('utilizador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('treino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.treino')),
            ],
            options={
                'unique_together': {('utilizador', 'treino')},
            },
        ),
    ]
