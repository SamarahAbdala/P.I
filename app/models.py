from django.db import models
from django.contrib.auth.models import User

# Função para definir um usuário padrão
class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    datanasc = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)

    def __str__(self):
        return self.nome  # Corrigido para usar 'nome' em vez de 'username'

# Forum
class Duvida(models.Model):
    titulo = models.CharField(max_length=255, default="Sem título")
    autor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    duvida = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Dúvidas"

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    duvida = models.ForeignKey(Duvida, related_name="comentarios", on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor} em '{self.duvida}'"
