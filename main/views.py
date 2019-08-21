import requests, json
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book, Post
from .forms import CommentForm, CommentUpdateForm

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

    def get_context_data(self, **kwargs):
        context = super(BookListview, self).get_context_data(**kwargs)
        book_list = Book.objects.all()
    
        page = self.request.GET.get('page', 1)
    
        paginator = Paginator(book_list, 4)
        try:
            books_view = paginator.page(page)
        except PageNotAnInteger:
            books_view = paginator.page(1)
        except EmptyPage:
            books_view = paginator.page(paginator.num_pages)
        context['books'] = books_view
        return context

@login_required
def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    user = request.user
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            c_form = Post(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                author=user,
                book=book,
                
            )
            c_form.save()
    # defining the form here again so it can clean the data after submit
    form = CommentForm()
    comments = Post.objects.filter(book=book)
    comment_count = comments.count()
    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json",
                                 params={"key": "Pan0ciQ093frutnmdDvug", "isbns": book.isbn})
    g_ratings = goodreads.json()["books"][0]["average_rating"]
    g_rating_counts = goodreads.json()["books"][0]["work_ratings_count"]
    context = {
        "comments": comments,
        "book": book,
        "form": form,
        "g_ratings": g_ratings,
        "g_rating_counts": g_rating_counts,
        "comment_count": comment_count
    }
    return render(request, "main/book_detail.html", context)

class PostDetailView(LoginRequiredMixin, DetailView):
   model = Post

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
       form.instance.user = self.kwargs.get('pk')
       return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   model = Post
   success_url = '/'

   def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def api(request, isbn):
    book_isbn = Book.objects.get(isbn=isbn)

    response = requests.get("https://www.goodreads.com/book/review_counts.json",
                            params={"key": "Pan0ciQ093frutnmdDvug", "isbns": book_isbn.isbn})
    data = response.json()['books'][0]

    if book_isbn is None:
        return JsonResponse({"error": "Inavalid ISBN"}), 404
        
    return JsonResponse({
        "title": book_isbn.title,
        "author": book_isbn.author,
        "isbn": book_isbn.isbn,
        "review_count": data['reviews_count'],
        "average_rating": data['average_rating']
    })    
