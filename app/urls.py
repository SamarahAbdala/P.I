from django.urls import path
from . import views  
from .views import (
    IndexView,
    lista_duvidas,
    cria_duvida,
    detalhes_duvida,
    edita_duvida,
    exclui_duvida,
    edita_comentario,
    exclui_comentario,
    editar_perfil,
    excluir_conta
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Página inicial
    path('', IndexView.as_view(), name='index'),

    # URLs de autenticação
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # URLs do Fórum
    path('duvidas/', lista_duvidas, name='lista_duvidas'),  # Lista de dúvidas
    path('duvidas/nova/', cria_duvida, name='cria_duvida'),  # Criar nova dúvida
    path('duvidas/<int:id>/', detalhes_duvida, name='detalhes_duvida'),  # Detalhes de uma dúvida
    path('duvidas/edita/<int:id>/', edita_duvida, name='edita_duvida'),  # Editar dúvida
    path('duvidas/exclui/<int:id>/', exclui_duvida, name='exclui_duvida'),  # Excluir dúvida

    # URLs de comentários
    path('comentario/<int:comentario_id>/edita/', edita_comentario, name='edita_comentario'),  # Editar comentário
    path('comentario/<int:comentario_id>/exclui/', exclui_comentario, name='exclui_comentario'),  # Excluir comentário

    # Quiz
    path('quiz/', views.quiz, name='quiz'),
    path('quiz-result/', views.quiz_result, name='quiz_result'),

    # URLs do perfil de usuário
    path('perfil/', views.perfil, name='perfil'),  # Perfil do usuário
    path('perfil/editar/', editar_perfil, name='editar_perfil'),  # Editar perfil
    path('perfil/excluir_conta/', excluir_conta, name='excluir_conta'),  # Excluir conta
]
