import requests, json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book, Post
from .forms import CommentForm, CommentUpdateForm



def home(request):

    context = {
        'books': Book.objects.all()
    }

    return render(request, 'main/home.html', context, {'title': 'Home'})

class BookListview(ListView):
    model = Book
    template_name = 'main/home.html'
    context_object_name = 'books'

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

    #def get_queryset(self):
    #    book_id = get_object_or_404(Book, id=self.kwargs.get('pk')) #getting the username from the url
    #    print('book_id')
    #    return Book.objects.filter(review=book_id).order_by('-date_posted')

#class PostListview(LoginRequiredMixin, ListView):
#    model = Post
#    template_name = 'main/book_detail.html'
#    context_object_name = 'posts'
#    ordering = ['-date_posted']

#def display_comment(request):
#    #book = Book.objects.get(pk=pk)
#    comments = Post.objects.all() #filter(book=book)
#    context = {
#        #"book": book,
#        "comments": comments
#    }
#    return render(request, "main/book_detail.html", context)


#class PostCreateview(LoginRequiredMixin, CreateView):
#   model = Post
#   fields = ['title', 'content']
#
#   def form_valid(self, form):
#       form.instance.book = self.kwargs.get('pk')
#       return super().form_valid(form)