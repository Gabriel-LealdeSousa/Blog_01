from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone #Importa tempo "TIME"
from taggit.managers import TaggableManager #Importa o gerenciador de tags do app taggit 

# Create your models here.
# 
class GerenciaPadroes(models.Manager):
    def get_queryset(self):
        return(
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )
    
class Post(models.Model): #Classe Post models.Model Cria uma tabela no Banco de dados

    class Status(models.TextChoices): #Classe aninhada para criar status de publicação
        DRAFT = 'DF', 'Draft' #Rascunho
        PUBLISHED = 'PB', 'Published' #Publicado
    
    
    titulo = models.CharField(max_length=250) #Titulo de 250 char etc.
    slug = models.SlugField(max_length=250, unique_for_date='publicado') #Slug é uma versão amigável do título do post
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE,
          related_name='blog_posts'
          )
    corpo = models.TextField()  #Texto longo para armazenar conteúdo do post
    publicado = models.DateTimeField(default=timezone.now) #modelo no db que cria a zona de tempo que a publicação foi lançada
    criado = models.DateTimeField(auto_now_add=True) #Data e hora automático
    atualizado = models.DateTimeField(auto_now=True)
    tags = TaggableManager() #Adicionando o gerenciador de tags do app taggit ao modelo Post
    status = models.CharField(

        max_length=2,
        choices=Status,
        default=Status.DRAFT) #Campo de status do post


    objects = models.Manager()
    published = GerenciaPadroes()

    class Meta: #Classe aninhada um só abre com o outro
        ordering = ['-publicado'] #Ordem do mais novo e antigos atrás deste
        indexes = [
        models.Index(fields=['-publicado']), #Cria índices para buscar os posts no BD
            ]
        


    def __str__(self):  #Como o objeto post será apresentado
        return self.titulo

    def get_absolute_url(self): #Retorna a URL do post
        return reverse(
            'blog:post_detail',
            args=[
                self.publicado.year,
                self.publicado.month,
                self.publicado.day,
                self.slug
            ]
                )

class Comment(models.Model): #Classe Comment models.Model Cria uma tabela no Banco de dados
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    nome = models.CharField(max_length=80)
    email = models.EmailField()
    corpo = models.TextField()
    criado = models.DateTimeField(auto_now_add=True)
    atualizado = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['criado']
        indexes = [
            models.Index(fields=['criado']),
        ]

    def __str__(self):
        return f'Comentário de {self.nome} em {self.post}'

    