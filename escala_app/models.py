from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    TIPO_USUARIO = [
        ('medico', 'Médico'),
        ('paciente', 'Paciente'),
    ]
    
    email = models.EmailField(unique=True)
    username = None
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'tipo']

    groups = models.ManyToManyField(Group, related_name="escala_app_users")
    user_permissions = models.ManyToManyField(Permission, related_name="escala_app_users_permissions")

    def is_medico(self):
        return self.tipo == 'medico'

    def is_paciente(self):
        return self.tipo == 'paciente'

# Modelo para Médicos
class Medico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="medico")
    crm = models.CharField(max_length=20, unique=True)
    especialidade = models.CharField(max_length=100)
    data_admissao = models.DateField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name} - {self.especialidade}"


# Modelo para Pacientes
class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="paciente")
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"


# Modelo de Postos de Atendimento
class Posto(models.Model):
    nome = models.CharField(max_length=130)
    endereco = models.CharField(max_length=250)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


# Modelo de Horários Disponíveis dos Médicos
class HorarioDisponivel(models.Model):
    medico = models.ForeignKey(Medico, related_name='horarios_disponiveis', on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=10, choices=[
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ])
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        return f"{self.medico} - {self.dia_semana} ({self.hora_inicio} - {self.hora_fim})"


# Modelo para Agendamento de Consultas
class Agendamento(models.Model):
    STATUS_AGENDAMENTO = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('realizado', 'Realizado'),
    ]

    medico = models.ForeignKey(Medico, related_name='agendamentos', on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, related_name='agendamentos', on_delete=models.CASCADE)
    posto = models.ForeignKey(Posto, related_name='agendamentos', on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_AGENDAMENTO, default='pendente')

    def __str__(self):
        return f"Consulta {self.paciente} com {self.medico} em {self.data} às {self.hora}"


# Modelo para Pagamentos e Assinaturas
class Assinatura(models.Model):
    medico = models.OneToOneField(Medico, on_delete=models.CASCADE, related_name='assinatura')
    plano = models.CharField(max_length=20, choices=[
        ('mensal', '$20/mês'),
        ('trimestral', '$50/trimestre'),
        ('anual', '$150/ano'),
    ])
    data_inicio = models.DateField(auto_now_add=True)
    data_expiracao = models.DateField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Plano {self.plano} - {self.medico}"


# Modelo para Integrações (Google Calendar, WhatsApp)
class Integracao(models.Model):
    medico = models.OneToOneField(Medico, on_delete=models.CASCADE, related_name='integracoes')
    google_calendar_token = models.CharField(max_length=255, blank=True, null=True)
    whatsapp_api_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Integrações de {self.medico}"
