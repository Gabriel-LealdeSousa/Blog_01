#segundo views verificar onde fica ele se é aqui mesmo
from django.shortcuts import get_object_or_404, render
from django.http import Http404

def post_detail(request, id):

    post = get_object_or_404(
      post,
       id=id,
       status=post.Status.PUBLICADO
       )

#entao tira o de baixo até return
    try:
            post = post.publicacao.get(id=id)
        
    except post.DoesNotExist:
            raise Http404("Post não encontrado!")
    
    return render(request,
        'blog/post/detalhe.html',
        {'post': post}
        )