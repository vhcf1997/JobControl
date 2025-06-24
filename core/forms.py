from django import forms
from .models import Job, Project

class JobForm(forms.ModelForm):
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