from django.core.paginator import EmptyPage, PageNotAnInteger , Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from .models import Post
from django.views.generic import ListView
from .forms import CommentForm, EmailPostForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )

def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (
                Post.published.annotate(
                search=SearchVector('titulo', 'corpo'),
            ).filter(search=query)
        )

    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )

class PostListView(ListView):
    queryset = Post.published.all() #Retorna todos os posts publicados
    context_object_name = 'posts'
    paginate_by = 3 #Paginação de 3 posts por página
    template_name = 'blog/post/list.html'

    def get_queryset(self):
        return Post.published.all() #Retorna todos os posts publicados
    
def post_share(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
        )

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = (
                f"{cd['name']} ({cd['email']}) "
            f"recomenda que você leia {post.titulo}"
            )

            message = (
            f"Leia {post.titulo} em {post_url}\n\n"
            f"read {post.titulo} at {post_url}\n\n"
            f"{cd['name']}\s' comments: {cd['comments']}"

            )

            send_mail(subject=subject, message=message, from_email=None, recipient_list=[cd['to']])

            sent = True

    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
        'post': post,
        'form': form,
        'sent': sent
        }
    )


def list_post(request, tag_slug=None):
    list_post = Post.published.all() #Retorna todos os posts publicados
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        list_post = list_post.filter(tags__in=[tag]) #Filtra os posts por tag
    paginator = Paginator(list_post, 3) #Paginação de 3 posts por página
    page_number = request.GET.get('page', 1) #Pega o número da página

    try:
        posts = paginator.page(page_number) #Retorna os posts da página atual

    except PageNotAnInteger:
        posts = paginator.page(1) #Retorna os posts da primeira página

    except EmptyPage:
        posts = paginator.page(paginator.num_pages) #Retorna os posts da última página
    
    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, 
        status=Post.Status.PUBLISHED,
        slug=post,
        publicado__year=year, 
        publicado__month=month, 
        publicado__day=day)

    comments = post.comments.filter(ativo=True) #Retorna os comentários ativos do post

    form = CommentForm() #Cria um formulário vazio

    post_tags_ids = post.tags.values_list('id', flat=True) #Retorna os ids das tags do post
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id) 
    #Acima Retorna os posts que possuem as mesmas tags do post atual, exceto o post atual
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
        ).order_by('-same_tags', '-publicado')[:4] #Ordena os posts pelo número de tags em comum e pela data de publicação, retornando os 4 primeiros
                                                                             

                                                                          
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})

def pagina_nao_encontrada(request, exception):
    return render(request, '404.html', status=404)