from django.views.generic import TemplateView, ListView, DetailView

from .models import Post

class  HelloWorld(TemplateView):
    template_name = 'test.html' # point to html file

class PostsView(ListView):
    model = Post
    template_name = 'home.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'