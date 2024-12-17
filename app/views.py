from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from .models import Duvida, Comentario, Usuario
from .forms import DuvidaForm, ComentarioForm, UserProfileForm
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# Importações Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.views import View
from .forms import (
    CustomUserCreationForm,

    )

from django.forms import *

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

@login_required
def lista_duvidas(request):
    duvidas = Duvida.objects.all()
    return render(request, 'forum/lista_duvidas.html', {'duvidas': duvidas})

@login_required
def detalhes_duvida(request, id):
    duvida = get_object_or_404(Duvida, id=id)
    comentarios = duvida.comentarios.all().order_by('-data_criacao')
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.duvida = duvida
            comentario.save()
            return redirect('detalhes_duvida', id=duvida.id)
    else:
        form = ComentarioForm()
    return render(request, 'forum/detalhes_duvida.html', {'duvida': duvida, 'comentarios': comentarios, 'form': form})

def cria_duvida(request):
    if request.method == 'POST':
        form = DuvidaForm(request.POST)
        if form.is_valid():
            # A validação do formulário está funcionando corretamente?
            titulo = form.cleaned_data['titulo']
            if Duvida.objects.filter(titulo=titulo).exists():
                messages.error(request, "Já existe uma dúvida com esse título.")
                return render(request, 'forum/cria_duvida.html', {'form': form})
            duvida = form.save(commit=False)
            duvida.autor = request.user
            duvida.save()
            messages.success(request, "Dúvida criada com sucesso!")
            return redirect('lista_duvidas')
    else:
        form = DuvidaForm()
    return render(request, 'forum/cria_duvida.html', {'form': form})


@login_required
def edita_duvida(request, id):
    duvida = get_object_or_404(Duvida, id=id)
    if request.user != duvida.autor and not request.user.is_staff:
        messages.error(request, "Você não tem permissão para editar esta dúvida.")
        return redirect('detalhes_duvida', id=duvida.id)
    if request.method == 'POST':
        form = DuvidaForm(request.POST, instance=duvida)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            if Duvida.objects.filter(titulo=titulo).exclude(id=duvida.id).exists():
                messages.error(request, "Já existe uma dúvida com esse título.")
                return render(request, 'forum/edita_duvida.html', {'form': form, 'duvida': duvida})
            form.save()
            messages.success(request, "Dúvida atualizada com sucesso!")
            return redirect('detalhes_duvida', id=duvida.id)
    else:
        form = DuvidaForm(instance=duvida)
    return render(request, 'forum/edita_duvida.html', {'form': form, 'duvida': duvida})

@login_required
def exclui_duvida(request, id):
    duvida = get_object_or_404(Duvida, id=id)
    if request.user != duvida.autor and not request.user.is_staff:
        messages.error(request, "Você não tem permissão para excluir esta dúvida.")
        return redirect('detalhes_duvida', id=duvida.id)
    if request.method == 'POST':
        duvida.delete()
        messages.success(request, "Dúvida excluída com sucesso!")
        return redirect('lista_duvidas')
    return render(request, 'forum/exclui_duvida.html', {'duvida': duvida})

@login_required
def edita_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, "Comentário atualizado com sucesso!")
            return redirect('detalhes_duvida', id=comentario.duvida.id)
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, 'forum/edita_comentario.html', {'form': form, 'duvida': comentario.duvida})

@login_required
def exclui_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user != comentario.autor and not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para excluir este comentário.")
        return redirect('detalhes_duvida', id=comentario.duvida.id)
    if request.method == 'POST':
        comentario.delete()
        messages.success(request, "Comentário excluído com sucesso!")
        return redirect('detalhes_duvida', id=comentario.duvida.id)
    return render(request, 'forum/exclui_comentario.html', {'comentario': comentario})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Usuário ou senha inválidos.")
        else:
            messages.error(request, "Dados inválidos.")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu com sucesso.")
    return redirect('index')

from django.shortcuts import render, redirect

# View para exibir o quiz
def quiz(request):
    return render(request, 'quiz.html')

# View para processar as respostas do quiz
def quiz_result(request):
    if request.method == 'POST':
        marca = request.POST.get('marca')
        publico = request.POST.get('publico')
        produto = request.POST.get('produto')
        
        # Dicionário com as combinações de respostas e URLs
        urls = {
            'Natura_Feminino_Perfume': 'https://www.natura.com.br/c/perfumaria-feminina',
            'Natura_Feminino_Presente': 'https://www.natura.com.br/c/presentes-feminino?iprom_id=ne-presentes_submenu&iprom_name=destaque3_presentes-feminino_30072024&iprom_creative=cat_presentes-feminino&iprom_pos=2',
            'Natura_Feminino_Corpo_e_Banho': 'https://www.natura.com.br/c/corpo-e-banho',
            'Natura_Masculino_Perfume': 'https://www.natura.com.br/c/perfumaria-masculina',
            'Natura_Masculino_Presente': 'https://www.natura.com.br/c/presentes-masculino?iprom_id=ne-presentes_submenu&iprom_name=destaque3_presentes-masculino_30072024&iprom_creative=cat_presentes-masculino&iprom_pos=1',
            'Natura_Masculino_Corpo_e_Banho': 'https://www.natura.com.br/c/homens-corpo-e-banho',
            'Natura_Infantil_Perfume': 'https://www.natura.com.br/c/infantil',
            'Natura_Infantil_Presente': 'https://www.natura.com.br/c/presentes-infantil?iprom_id=ne-presentes_submenu&iprom_name=destaque3_presentes-infantil_22102024&iprom_creative=cat_presentes-infantil&iprom_pos=3',
            'Natura_Infantil_Corpo_e_Banho': 'https://www.natura.com.br/c/infantil-corpo-e-banho',
            'Natura_Unissex_Perfume': 'https://www.natura.com.br/c/perfumaria-todo-mundo',
            'Natura_Unissex_Presente': 'https://www.natura.com.br/c/presentes',
            'Natura_Unissex_Corpo_e_Banho': 'https://www.natura.com.br/c/corpo-e-banho',
            'Avon_Feminino_Perfume': 'https://www.avon.com.br/c/perfumaria-feminino',
            'Avon_Feminino_Presente': 'https://www.avon.com.br/c/presentes-para-quem-para-feminino',
            'Avon_Feminino_Corpo_e_Banho': 'https://www.avon.com.br/c/cuidados-diarios',
            'Avon_Masculino_Perfume': 'https://www.avon.com.br/c/perfumaria-masculino',
            'Avon_Masculino_Presente': 'https://www.avon.com.br/c/presentes-para-quem-para-masculino',
            'Avon_Masculino_Corpo_e_Banho': 'https://www.avon.com.br/s/produtos?busca=masculino&cgid_filter=cuidados-diarios',
            'Avon_Infantil_Perfume': 'https://www.avon.com.br/c/perfumaria-infantil',
            'Avon_Infantil_Presente': 'https://www.avon.com.br/s/produtos?busca=infantil',
            'Avon_Infantil_Corpo_e_Banho': 'https://www.avon.com.br/c/cuidados-diarios-infantil',
            'Avon_Unissex_Perfume': 'https://www.avon.com.br/c/perfumaria',
            'Avon_Unissex_Presente': 'https://www.avon.com.br/c/presentes-para-quem-para-todas-as-pessoas',
            'Avon_Unissex_Corpo_e_Banho': 'https://www.avon.com.br/c/cuidados-diarios',
            'Boticario_Feminino_Perfume': 'https://www.boticario.com.br/perfumaria/feminino/',
            'Boticario_Feminino_Presente': 'https://www.boticario.com.br/presentes/feminino/',
            'Boticario_Feminino_Corpo_e_Banho': 'https://www.boticario.com.br/corpo-e-banho/',
            'Boticario_Masculino_Perfume': 'https://www.boticario.com.br/perfumaria/masculino/',
            'Boticario_Masculino_Presente': 'https://www.boticario.com.br/presentes/masculino/',
            'Boticario_Masculino_Corpo_e_Banho': 'https://www.boticario.com.br/cuidados-masculinos/',
            'Boticario_Infantil_Perfume': 'https://www.boticario.com.br/perfumaria/infantil/',
            'Boticario_Infantil_Presente': 'https://www.boticario.com.br/presentes/crianca/',
            'Boticario_Infantil_Corpo_e_Banho': 'https://www.boticario.com.br/corpo-e-banho/infantil/',
            'Boticario_Unissex_Perfume': 'https://www.boticario.com.br/perfumaria/unissex/',
            'Boticario_Unissex_Presente': 'https://www.boticario.com.br/presentes/',
            'Boticario_Unissex_Corpo_e_Banho': 'https://www.boticario.com.br/corpo-e-banho/',
        }
        
        # Monta a chave para o dicionário
        key = f'{marca}_{publico}_{produto}'
        url = urls.get(key, '/')
        
        return redirect(url)
    else:
        return redirect('quiz')

@login_required
def excluir_conta(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.delete()  
            messages.success(request, "Sua conta foi excluída com sucesso.")
            return redirect('/')  # Redireciona para a página inicial após a exclusão
        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao excluir sua conta: {e}")
            return redirect('perfil')  # Redireciona de volta para a página do perfil caso erro

    return redirect('/')

@login_required
def editar_perfil(request):
    usuario = request.user.usuario  
    user = request.user 

    if request.method == "POST":
        if 'nome' in request.POST:
            usuario.nome = request.POST['nome']
        if 'datanasc' in request.POST:
            usuario.datanasc = request.POST['datanasc']
        if 'cpf' in request.POST:
            usuario.cpf = request.POST['cpf']
        
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save() 
        
        usuario.save() 
        return redirect('perfil') 

    return render(request, 'perfil/editar_perfil.html', {'usuario': usuario, 'user': user})

def perfil(request):
    if request.user.is_authenticated:
        try:
            # Tente acessar o objeto Usuario relacionado ao User
            usuario = request.user.usuario
            usuario_nao_encontrado = False
        except Usuario.DoesNotExist:
            # Caso não exista, defina a variável para mostrar que o superusuário não tem um 'usuario'
            usuario = None
            usuario_nao_encontrado = True

        return render(request, 'perfil/perfil.html', {
            'usuario': usuario,
            'usuario_nao_encontrado': usuario_nao_encontrado
        })
    else:
        return redirect('login')


# Registro de Usuário
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automaticamente após o registro
            return redirect('index')  # Redireciona para a página de perfil após o registro
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})