from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CommentForm
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
def post_list(request):
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 5)  # 5 постов на страницу

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    # posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post_detail', post_id=post.id)
        elif 'like submit' in request.POST:
            if request.user in post.likes.all():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            return redirect('post_detail', post_id=post.id)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'is_liked': request.user in post.likes.all() if request.user.is_authenticated else False,
        'total_likes': post.likes.count()
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            #form.save()
            post = form.save(commit=False)  # не сохраняем объект в базу данных сразу
            post.author = request.user      # назначаем автора
            post.save()                     # теперь сохраняем
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')

    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden()

    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('post_detail', post_id=post.id)
    return render(request, 'blog/edit_post.html', {'form':form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/delete_post.html',{'post': post})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form})

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_liked = False

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        is_liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'is_liked': is_liked,
            'total_likes': post.likes.count()
        })

    return redirect('post_detail', post_id=post.id)