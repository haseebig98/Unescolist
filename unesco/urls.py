from django.urls import path, reverse_lazy
from . import views

app_name='unesco'

urlpatterns = [
    path('', views.sites_list, name='sites_list'),
    path('favorites/', views.MyFavoritesView.as_view(), name='my_favorites'),
    path('site/<int:site_id>/', views.site_detail, name='site_detail'),
    # path('site/<int:site_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('site/<int:site_id>/comment', views.CommentCreateView.as_view(), name='site_comment_create'),
    path('comment/<int:pk>/delete', views.CommentDeleteView.as_view(success_url=reverse_lazy('unesco:sites_list')), name='site_comment_delete'),
    path('site/<int:site_id>/favorite', views.AddFavoriteView.as_view(), name='site_favorite'),
    path('site/<int:site_id>/unfavorite', views.DeleteFavoriteView.as_view(), name='site_unfavorite'),
]
