# django shortcuts, class based view and urls redirection module
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy, reverse
from django.http import  JsonResponse
from django.db.models import Prefetch

# application module
from .models import Post, Comment
from .forms import UserRegistrationForm, PostForm, CommentForm

# django contrib package modules
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib import messages

# decorator, mixins and user made decorator and mixins
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators_mixins import only_admin, OnlyAdmin, DeleteCommentMixin

from django.utils import timezone


###########  POST  ##############
class PostListView(LoginRequiredMixin, ListView):   # list all the post
    model = Post
    context_object_name = 'posts'
    template_name = 'index.html'
    login_url = 'login'

    def get_queryset(self):
            return Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')


class PostDetailView(LoginRequiredMixin,DetailView):  # post detail
    login_url = 'login'
    model = Post
    template_name = 'post/detail_post.html'
    context_object_name = 'post'

class PostCreateView(OnlyAdmin, CreateView):
    login_url = 'login'
    form_class = PostForm
    model = Post
    template_name = 'post/create_post.html'

    def handle_no_permission(self):
        return redirect('about')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(OnlyAdmin, UpdateView):
    login_url = 'login'
    form_class = PostForm
    model = Post
    template_name = 'post/update_post.html'

    def handle_no_permission(self):
        return redirect('about')


class PostDeleteView(OnlyAdmin, DeleteView):
    login_url = 'login'
    model = Post
    template_name = 'post/delete_post.html'
    success_url = reverse_lazy('home')

    def handle_no_permission(self):
        return redirect('about')

    # if recently deleted post has publish date then it open home, if not then
    # it opens draft list
    def get_success_url(self,*args, **kwargs):
        if self.get_object().publish_date:
           return reverse_lazy("home")
        else:
           return reverse_lazy('post_draft_list')


class DraftListView(OnlyAdmin, ListView):   # list all the post
      login_url = 'login'
      model = Post
      template_name = "post/post_draft_list.html"
      context_object_name = 'posts'

      def handle_no_permission(self):
          return redirect('about')

      def get_queryset(self):
              return Post.objects.filter(publish_date__isnull=True).order_by('-create_date')


@only_admin
def post_publish(request, test_pk):
    post = get_object_or_404(Post, id=test_pk)
    post.publish()
    return redirect('home')


############## comment ###########

class CommentCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    form_class = CommentForm
    model = Comment
    template_name = 'comment/create_comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['pk'])
        # we insert the value of post which present in class Comment
        return super().form_valid(form)


class CommentDeleteView(DeleteCommentMixin, DeleteView):
    login_url = 'login'
    model = Comment
    # template_name = 'comment/delete_comment.html'
    context_object_name = "comment"

    def post(self, request, *args, **kwargs):
        self.get_object().delete()
        data = {'deleted': True }
        return JsonResponse(data)

    def get_success_url(self,*args, **kwargs):
        post_id = self.get_object().post.id
        return reverse_lazy('detail', kwargs={'pk':post_id})

############## login and logout #############

def user_registration(request):
     if not request.user.is_authenticated:
         form = UserRegistrationForm()
         if request.method == "POST":
             form = UserRegistrationForm(request.POST)

             if form.is_valid():
                 user = form.save()
                 username = form.cleaned_data.get('username')
                 messages.success(request, f"user register successfully  + {username}")

                 # add to Group
                 normal_user_group = Group.objects.get(name='normal_user')
                 user.groups.add(normal_user_group)

                 return redirect('login')
             else:
                 print("error")
         return render(request, 'register.html', context={'form': form})

     else:
         return redirect('home')

def user_login(request):
   if not request.user.is_authenticated:
      if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')

         user = authenticate(request, username=username, password=password)

         if user:
             login(request, user)
             return redirect('home')
         else:
             messages.info(request, "username or password is invalid")

      return render(request, 'login_form.html', context={})
   else:
      return redirect('home')


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


########  other ##############

@login_required(login_url='login')
def about(request):   # info about the blog
    return render(request, 'about.html', context={})

@login_required(login_url='login')
def like(request, *args, **kwargs):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        post_id = kwargs["pk"]

        post = get_object_or_404(Post, id=post_id)

        # true if user already_liked the post else false
        flag = request.user in post.likes.all()

        if int(request.POST.get('button_click')):
            if flag:
                #  user already like post
                post.likes.remove(request.user)
                flag = False
            else:
                # user not already like post
                post.likes.add(request.user)
                flag = True

        data2 = {"liked": flag}
        return JsonResponse(data2)

    # some error occured
    return JsonResponse({"error": "Please Retry.."}, status=400)
