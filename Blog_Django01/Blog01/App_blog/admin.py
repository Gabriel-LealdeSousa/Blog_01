from django.contrib import admin
from .models import Comment, Post



@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'slug', 'autor', 'publicado', 'status']
    list_filter = ['status', 'criado', 'publicado', 'autor']
    search_fields = ['titulo', 'corpo']
    prepopulated_fields = {'slug': ('titulo',)}
    raw_id_fields = ['autor']
    date_hierarchy = 'publicado'
    ordering = ['status', 'publicado']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'post', 'criado', 'ativo']
    list_filter = ['ativo', 'criado', 'atualizado']
    search_fields = ['nome', 'email', 'corpo']


