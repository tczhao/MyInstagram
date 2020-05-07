from annoying.decorators import ajax_request
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Post, Like, InstagramUser

# from django.contrib.auth.forms import UserCreationForm
from Instagram.forms import CustomerUserCreationForm
from Instagram.models import UserConnection

from django.contrib.auth.mixins import LoginRequiredMixin

class  HelloWorld(TemplateView):
    template_name = 'test.html' # point to html file

class PostsView(ListView):
    model = Post
    template_name = 'index.html'
    
    def get_queryset(self):
        current_user = self.request.user
        if str(current_user) == "AnonymousUser":
            # return super(PostsView, self).get_queryset()
            return Post.objects.all().order_by('-posted_on')[:20]
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)[:20]

class UserDetailView(DetailView):
    model = InstagramUser
    template_name = 'user_detail.html'

class UserEditView(LoginRequiredMixin, UpdateView):
    model = InstagramUser
    template_name = 'user_edit.html'
    fields = ['profile_picture', 'username']
    login_url = 'login'

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

@ajax_request
def toggleFollow(request):
    current_user = InstagramUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstagramUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }

class ExploreView(ListView):
    model = Post
    template_name = 'explore.html'

    login_url = 'login'

    def get_queryset(self):
        return Post.objects.all().order_by('-posted_on')[:20]
