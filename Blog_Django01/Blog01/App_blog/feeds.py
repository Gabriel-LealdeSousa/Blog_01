import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class UltimasPublicacoes(Feed):
    title = 'Blog01'
    link = reverse_lazy('blog:post_list')
    description = 'Novidades do Blog'

    def items(self):
        return Post.publicados.all()[:5]

    def item_title(self, item):
        return item.titulo

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.corpo), 30)

    def item_pubdate(self, item):
        return item.publish

    