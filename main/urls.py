#
from django.urls import path
from .views import BookListview, BookDetailview, PostCreateview
from . import views

urlpatterns = [
    path('', BookListview.as_view(), name='main-home'),
    path('book/<int:pk>/', BookDetailview.as_view(), name='book-detail'),
    path('book/<int:pk>/new', PostCreateview.as_view(), name='post-create'),
]