from django.db.models.fields import return_None
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import  login_required
from core.models import *
from django.db.models import Sum, Max
from .forms import *
from django.contrib.auth.forms import UserCreationForm # <-- ADICIONAR ESTA IMPORTAÇÃO
from django.contrib.auth import login # <-- ADICIONAR ESTA IMPORTAÇÃO, para logar o usuário após o registro
from django.contrib import messages
from datetime import datetime # <-- ADICIONE ESTA LINHA para trabalhar com datas
import calendar # <-- ADICIONE ESTA LINHA para obter nomes de meses
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        # Se o usuário estiver logado, redireciona para a lista de trabalhos
        return redirect('core:listar_trabalhos')
    else:
        # Se não estiver logado, exibe uma página de boas-vindas
        context = {
            'page_title': 'Bem-vindo ao Controle de Horas',
        }
        return render(request, 'core/index.html', context)

# --------------------- CRUD trabalhos -----------------------------------------------------
@login_required
def lista_trabalhos(request):
    jobs = Job.objects.filter(user=request.user)

    # Lógica de Filtro por Mês e Ano (Já existente)
    current_year = datetime.now().year
    current_month = datetime.now().month

    selected_year = request.GET.get('year', str(current_year))
    selected_month = request.GET.get('month', str(current_month))

    try:
        selected_year_int = int(selected_year)
        selected_month_int = int(selected_month)
    except (ValueError, TypeError):
        selected_year_int = current_year
        selected_month_int = current_month
        messages.warning(request, "Parâmetros de data inválidos. Exibindo dados do mês atual.")

    jobs = jobs.filter(date__year=selected_year_int, date__month=selected_month_int)

    # --- Lógica para Ordenação (NOVO) ---
    # Pega o parâmetro 'order' da URL. O padrão é '-date' (decrescente por data).
    sort_order_param = request.GET.get('order', '-date')

    # Validação básica para o parâmetro de ordenação
    # Garante que apenas 'date' ou '-date' sejam usados, prevenindo inputs maliciosos
    if sort_order_param not in ['date', '-date']:
        sort_order_param = '-date' # Volta para o padrão seguro se for inválido

    # Aplica a ordenação ao QuerySet
    # A ordenação secundária por 'project__name' é para o caso de datas iguais
    jobs = jobs.order_by(sort_order_param, 'project__name')

    # Cálculo do total de horas (Já existente)
    total_hours_sum = jobs.aggregate(total_hours_sum=Sum('hours_worked'))['total_hours_sum']
    if total_hours_sum is None:
        total_hours_sum = 0.00

    # Listas de anos e meses para os dropdowns (Já existente)
    years = range(datetime.now().year - 5, datetime.now().year + 2) # Ex: 2020 a 2026
    months_pt_br = [
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
        (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
        (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
    ]

    # Lógica para o botão "Registros Mais Recentes" (Já existente)
    most_recent_job_date = None
    most_recent_month = None
    most_recent_year = None
    if Job.objects.filter(user=request.user).exists():
        latest_date_agg = Job.objects.filter(user=request.user).aggregate(max_date=Max('date'))
        if latest_date_agg['max_date']:
            most_recent_job_date = latest_date_agg['max_date']
            most_recent_month = most_recent_job_date.month
            most_recent_year = most_recent_job_date.year

    context = {
        'jobs': jobs,
        'page_title': 'Controle de Horas',
        'total_hours_sum': total_hours_sum,
        'years': years,
        'months': months_pt_br,
        'selected_year': str(selected_year_int),
        'selected_month': str(selected_month_int),
        'most_recent_month': str(most_recent_month) if most_recent_month else None,
        'most_recent_year': str(most_recent_year) if most_recent_year else None,
        # --- NOVO: Variáveis para controle de ordenação no template ---
        'current_order': sort_order_param, # Passa a ordem atual (ex: '-date' ou 'date')
        # Define qual será a próxima ordem ao clicar no botão
        'next_order': 'date' if sort_order_param == '-date' else '-date',
    }
    return render(request, 'core/job_list.html', context)


@login_required
def add_trabalhos(request):
    if request.method == 'POST':
        # Passa o usuário logado para o formulário
        form = JobForm(request.POST, user=request.user) # <-- ALTERADO AQUI
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            messages.success(request, 'Entrada de trabalho adicionada com sucesso!')
            return redirect('core:listar_trabalhos')
    else:
        # Passa o usuário logado para o formulário (para a lista de projetos)
        form = JobForm(user=request.user) # <-- ALTERADO AQUI

    context = {
        'form': form,
        'page_title': 'Adicionar Nova Entrada de Trabalho',
    }
    return render(request, 'core/job_form.html', context)

@login_required
def editar_trabalhos(request, pk):
    job = get_object_or_404(Job, pk=pk, user=request.user) # Garante que só o dono edite

    if request.method == 'POST':
        # Passa o usuário logado para o formulário
        form = JobForm(request.POST, instance=job, user=request.user) # <-- ALTERADO AQUI
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrada de trabalho atualizada com sucesso!')
            return redirect('core:listar_trabalhos')
    else:
        # Passa o usuário logado para o formulário
        form = JobForm(instance=job, user=request.user) # <-- ALTERADO AQUI

    context = {
        'form': form,
        'page_title': f'Editar Entrada de Trabalho - {job.project.name} ({job.date.strftime("%d/%m/%Y")})',
        'job': job,
    }
    return render(request, 'core/job_form.html', context)

@login_required
def delete_trabalhos(request, pk):
    job = get_object_or_404(Job, pk=pk, user=request.user)

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Entrada de trabalho excluída com sucesso!') # <-- ADICIONE ESTA MENSAGEM
        return redirect('core:listar_trabalhos')

    context = {
        'job': job,
        'page_title': 'Confirmar Exclusão de Trabalho',
    }
    return render(request, 'core/job_confirm_delete.html', context)




# --------------------- CRUD projetos -----------------------------------------------------
@login_required
def lista_projetos(request):
        # Apenas projetos do usuário logado
        projects = Project.objects.filter(user=request.user).annotate(
            # CORREÇÃO AQUI: Use 'job' em vez de 'job_set'
            total_hours=Sum('job__hours_worked')  # <--- ALTERADO AQUI
        ).order_by('name')

        context = {
            'projects': projects,
            'page_title': 'Meus Projetos',
        }
        return render(request, 'core/project_list.html', context)

def add_projetos(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False) # Não salva ainda
            project.user = request.user # Atribui o usuário logado ao projeto
            project.save() # Agora salva
            messages.success(request, 'Projeto adicionado com sucesso!')
            return redirect('core:listar_projetos') # Redireciona para a lista de projetos
        else:
            messages.error(request, 'Erro ao adicionar projeto. Verifique os campos.')
    else:
        form = ProjectForm() # Formulário vazio para GET

    context = {
        'form': form,
        'page_title': 'Adicionar Novo Projeto',
    }
    return render(request, 'core/project_form.html', context)

def editar_projetos(request, pk):
    # Busca o projeto, mas APENAS SE ELE PERTENCER AO USUÁRIO LOGADO.
    # Se o ID não for do usuário, retorna 404 (segurança).
    project = get_object_or_404(Project, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto atualizado com sucesso!')
            return redirect('core:listar_projetos')
        else:
            messages.error(request, 'Erro ao atualizar projeto. Verifique os campos.')
    else:
        form = ProjectForm(instance=project)  # Preenche o formulário com dados existentes

    context = {
        'form': form,
        'page_title': f'Editar Projeto - {project.name}',
        'project': project,
    }
    return render(request, 'core/project_form.html', context)

def delete_projetos(request, pk):
    # Busca o projeto para deletar, mas APENAS SE ELE PERTENCER AO USUÁRIO LOGADO.
    project = get_object_or_404(Project, pk=pk, user=request.user)

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Projeto excluído com sucesso!')
        return redirect('core:listar_projetos')

    context = {
        'project': project,
        'page_title': 'Confirmar Exclusão de Projeto',
    }
    return render(request, 'core/project_confirm_delete.html', context)

# --------------------- Registro de usuario -----------------------------------------------------

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada e login realizado com sucesso!') # <-- ADICIONE ESTA MENSAGEM
            return redirect('core:listar_trabalhos')
        else: # Se o formulário não for válido, você pode adicionar uma mensagem de erro
            messages.error(request, 'Por favor, corrija os erros no formulário de registro.')
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'page_title': 'Registrar Nova Conta',
    }
    return render(request, 'registration/register.html', context)