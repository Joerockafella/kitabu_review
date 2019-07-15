from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Book, Post

#def home(request):
#
#    context = {
#        'books': Book.objects.all()
#    }
#
#    return render(request, 'main/home.html', context, {'title': 'Home'})

class BookListview(ListView):
    model = Book
    template_name = 'main/home.html'
    context_object_name = 'books'


class BookDetailview(DetailView):
    model = Book
    fields = ['title', 'content']


class PostCreateview(CreateView):
    model = Post
    fields = ['title', 'content']
