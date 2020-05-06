from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Post, Like

# from django.contrib.auth.forms import UserCreationForm
from Instagram.forms import CustomerUserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin

class  HelloWorld(TemplateView):
    template_name = 'test.html' # point to html file

class PostsView(ListView):
    model = Post
    template_name = 'index.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__' # user need to input all fields
    login_url = 'login'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title'] # user can only update title

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    # no field, due its delete action
    success_url = reverse_lazy("posts")

class SignUp(CreateView):
    # form_class = UserCreationForm # default form
    form_class = CustomerUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")


@ajax_request # so that this function renders to ajax request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }