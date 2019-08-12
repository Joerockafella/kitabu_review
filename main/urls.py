#
from django.urls import path
from .views import BookListview, PostDetailView, PostUpdateView, PostDeleteView
from . import views


urlpatterns = [
    path('', BookListview.as_view(), name='main-home'),
    path('book/<int:pk>/', views.book_detail, name='book-detail'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('api/<str:isbn>/', views.api),
]