from django.contrib import admin
from .models import Usuario, Duvida, Comentario

# Modelo de Usuário
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('idUsuario', 'nome', 'email', 'datanasc', 'cpf', 'user')  # Campos a exibir na lista de usuários
    search_fields = ('nome', 'email', 'cpf')  # Campos para pesquisa rápida
    list_filter = ('datanasc',)  # Filtro para exibir por data de nascimento

# Modelo de Duvida
class DuvidaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_envio')  # Campos a exibir na lista de dúvidas
    search_fields = ('titulo', 'duvida')  # Campos para pesquisa
    list_filter = ('data_envio', 'autor')  # Filtros para o painel de administração

# Modelo de Comentario
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('duvida', 'autor', 'data_criacao')  # Campos a exibir na lista de comentários
    search_fields = ('texto', 'autor__username')  # Campos para pesquisa
    list_filter = ('data_criacao', 'autor')  # Filtros para o painel de administração

# Registro dos modelos no painel de administração
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Duvida, DuvidaAdmin)
admin.site.register(Comentario, ComentarioAdmin)
