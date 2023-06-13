from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User

from taggit.models import Tag

from general.functions import get_auto_id
from .models import BlogPost, Comment, Notification
from .forms import BlogPostForm, BlogPostSearchForm, CommentForm


@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.auto_id = get_auto_id(BlogPost)
            post.creator = request.user
            post.updater = request.user
            post.save()
            form.save_m2m()

            return redirect('blogs:blog_post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    
    context = {'form': form}

    return render(request, 'blogs/create_blog_post.html', context)


@login_required
def edit_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, creator=request.user, is_deleted=False)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updater = request.user
            post.date_updated = timezone.now()
            post.save()
            form.save_m2m()

            return redirect('blogs:blog_post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    
    context = {'form': form, 'post': post}

    return render(request, 'blogs/edit_blog_post.html', context)


@login_required
def blog_post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, is_deleted=False)
    comments = post.comments.filter(is_deleted=False)
    tags = post.tags.all()

    context = {
        'post': post, 
        'comments': comments,
        'tags': tags,
    }

    return render(request, 'blogs/blog_post_detail.html', context)


@login_required
def blog_post_list(request):
    posts = BlogPost.objects.filter(is_deleted=False)
    tags = Tag.objects.all()

    query = request.GET.get('q')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    
    tag = request.GET.get('tag')
    if tag:
        posts = posts.filter(tags__name__in=[tag])


    context = {
        'posts': posts,
        'query': query,
        'tags': tags,
    }

    return render(request, 'blogs/blog_post_list.html', context)


@login_required
def create_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, is_deleted=False)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.auto_id = get_auto_id(Comment)
            comment.creator = request.user
            comment.updater = request.user
            comment.post = post
            comment.save()

            return redirect('blogs:blog_post_detail', pk=pk)
    else:
        form = CommentForm()

    context = {'form': form, 'post': post}

    return render(request, 'blogs/create_comment.html', context)


@login_required
def author_profile(request, pk):
    author = get_object_or_404(User, pk=pk)
    posts = author.creator_blogpost_objects.filter(is_deleted=False)

    context = {'author': author, 'posts': posts}

    return render(request, 'blogs/author_profile.html', context)


@login_required
def blog_post_search(request):
    form = BlogPostSearchForm(request.GET)
    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')

        blog_posts = BlogPost.objects.filter(is_deleted=False)

        if keyword:
            blog_posts = blog_posts.filter(title__icontains=keyword)

        context = {
            'form': form,
            'blog_posts': blog_posts,
        }

        return render(request, 'blogs/blog_post_search.html', context)
    
    context = {
        'form': form,
    }

    return render(request, 'blogs/blog_post_search.html', context)


@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, is_read=False, is_deleted=False)

    context = {'notifications': notifications}

    return render(request, 'blogs/notifications.html', context)




