from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import SignUpForm,CommentForm ,PostForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

def post_list(request):
    posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')
    return render(request, 'blog/post_list.html' , {'posts': posts})
def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method=='POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post':post , 'comments':comments , 'form':form})

def signup(request):
    if request.method== "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.SUCCESS(request,"kayıt başarılı! giriş yapabilirsiniz")
            return redirect('post_list')
        else:
            messages.ERROR(request,"hatalı veri girişi!")
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html',{'form' : form}) 

@login_required
def post_new(request):
    if request.method=='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_at= timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form=PostForm()
    return render(request, 'blog/post_edit.html',{'form':form})

class SignUpView(generic.CreateView):
    form_class=UserCreationForm
    success_url=reverse_lazy('post_list')
    template_name='registration/signup.html'

        


# Create your views here.
