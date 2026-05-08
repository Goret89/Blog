from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Vote, Profile
from .forms import PostForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CommentForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.db.models import Count, Q


# Create your views here.
def post_list(request):
    posts = Post.objects.all()

    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    author = request.GET.get('author')
    if author:
        posts = posts.filter(author__username__icontains=author)

    tag = request.GET.get('tag')
    if tag:
        posts = posts.filter(tags__name=tag)

    posts = posts.annotate(likes=Count('votes', filter=Q(votes__value=1)))

    sort = request.GET.get('sort')

    if sort == 'popular':
        posts = posts.order_by('-likes')
    else:
        posts = posts.order_by('-created_at')

    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    form = CommentForm()

    user_vote = None
    if request.user.is_authenticated:
        vote = post.votes.filter(user=request.user).first()
        user_vote = vote.value if vote else None

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post_detail', post_id=post.id)

        elif 'vote' in request.POST:
            value = int(request.POST.get('value'))  # 1 or -1

            vote, created = Vote.objects.get_or_create(
                user=request.user,
                post=post,
                defaults={'value': value}
            )

            if not created:
                if vote.value == value:
                    vote.delete()  # delete vote
                else:
                    vote.value = value
                    vote.save()

            return redirect('post_detail', post_id=post.id)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'user_vote': user_vote,
        'total_likes': post.likes_count(),
        'total_dislikes': post.dislikes_count(),
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # don't save object immediately to the DB
            post.author = request.user      # assign the author
            post.save()                     # saving
            form.save_m2m()
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
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        post_id = comment.post.id
        comment.delete()
        return redirect('post_detail', post_id=post_id)
    return redirect('post_list')


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
            'total_likes': post.likes_count()
        })

    return redirect('post_detail', post_id=post.id)


@login_required
def vote_view(request, post_id):
    post = Post.objects.get(id=post_id)
    value = int(request.POST.get('value')) # 1 or -1

    vote, created = Vote.objects.get_or_create(
        user=request.user,
        post=post,
        defaults={'value': value}
    )

    user_vote = None

    if not created:
        if vote.value == value:
            vote.delete()
            user_vote = None
        else:
            vote.value = value
            vote.save()
            user_vote = value
    
    else:
        user_vote = value

    return JsonResponse({
        'likes': post.likes_count(),
        'dislikes': post.dislikes_count(),
        'user_vote': user_vote
    })

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    posts = Post.objects.filter(author=user).order_by('-created_at')

    return render(request, 'blog/profile.html', {
        'profile_user': user,
        'profile': profile,
        'posts': posts
    })


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'blog/edit_profile.html', {'form': form})