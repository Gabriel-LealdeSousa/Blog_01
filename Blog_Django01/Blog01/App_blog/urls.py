from django.urls import path
from . import views
from .feeds import UltimasPublicacoes

app_name = 'blog'


urlpatterns = [ #Não adicionar blog no '' da path abaixo.
    path('', views.list_post, name='list_post'), #Add Blog01/App_blog/urls.py
    #path('', views.PostListView.as_view(), name='list_post'),
    path('tag/<slug:tag_slug>/', views.list_post, name='list_post_by_tag'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'
        ),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('feeds/', UltimasPublicacoes(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]