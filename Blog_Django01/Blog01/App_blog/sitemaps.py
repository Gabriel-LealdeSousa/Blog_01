from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        from .models import Post
        return Post.published.all()

    def lastmod(self, obj):
        return obj.atualizado

    