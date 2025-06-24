from django import forms
from .models import Job, Project

class JobForm(forms.ModelForm):
    # NOVO: Adicione o construtor __init__ para filtrar o queryset de projetos
    def __init__(self, *args, **kwargs):
        # Obtém o 'user' dos kwargs antes de chamar o construtor pai
        # Remova 'user' de kwargs para não passar para o super().__init__
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filtra o queryset do campo 'project' para mostrar apenas os projetos do usuário
        if user:
            self.fields['project'].queryset = Project.objects.filter(user=user).order_by('name')
        else:
            # Se, por algum motivo, o usuário não for passado,
            # garanta que o queryset esteja vazio ou mostre um erro.
            self.fields['project'].queryset = Project.objects.none() # Impede que projetos de outros apareçam

    class Meta:
        model = Job
        fields = ['date', 'project', 'description', 'hours_worked']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'hours_worked': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'date': 'Data do Trabalho',
            'project': 'Projeto Associado',
            'description': 'Descrição Detalhada',
            'hours_worked': 'Horas Trabalhadas (Ex: 8.5)',
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'name': 'Nome do Projeto',
            'description': 'Descrição do projeto',
        }