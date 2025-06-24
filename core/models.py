from django.db import models
from django.contrib.auth.models import User # Importa o modelo User do Django

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    # CORREÇÃO AQUI: Remova 'unique=True'
    name = models.CharField(max_length=200, verbose_name="Nome do Projeto")
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição do Projeto"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado Em")

    def __str__(self):
        # Sugestão: Alterar para uma representação mais informativa no Admin
        # return self.name # Seu código atual
        return f"{self.name} (por {self.user.username})" # Mais claro para diferenciar projetos com o mesmo nome

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos" # Corrigi para verbose_name_plural, se não for typo
        ordering = ['name'] # Ordena os projetos por nome
        unique_together = ('user', 'name') # <--- ESTA É A ÚNICA RESTRIÇÃO DE UNICIDADE QUE DEVE EXISTIR
                                          # Para permitir nomes duplicados entre usuários diferentes
class Job(models.Model):
    # Busca usuário cadastrado
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Usuário poderá cadastrar projetos e depois filtrar por eles
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    date = models.DateField(verbose_name="Data")

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição de Atividades',
    )
    # Horas trabalhadas por dia, então 24 horas é o máximo
    hours_worked = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00,
        verbose_name="Horas Trabalhadas",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado Em")

    def __str__(self):
        # Representação legível no Admin
        return f"{self.user.username} - {self.project.name} - {self.date.strftime('%d/%m/%Y')} - {self.hours_worked}h"

    class Meta:
        verbose_name = "Trabalho"
        verbose_name_plural = "Trabalhos"
        ordering = ['-date', 'project__name']  # Ordenar por data (mais recente) e depois por nome do projeto