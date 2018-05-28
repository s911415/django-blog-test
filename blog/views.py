from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from blog.models import *
from .forms import PostForm


class PostView:
    # Create your views here.
    @staticmethod
    def post_list(request):
        posts = Post.objects.order_by('-published_date').all()
        return render(request, 'blog/post_list.html', {'posts': posts})

    @staticmethod
    def index(request):
        return render(request, 'blog/index.html', {})

    @staticmethod
    def show_post(request, id: int):
        post = get_object_or_404(Post, pk=id)
        comments = post.comments.order_by('-id').all()
        return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

    @staticmethod
    def do_comment(request):
        if request.method == 'POST':
            id = request.POST.get('id')
            name = request.POST.get('name')
            text = request.POST.get('content')
            Comment.objects.create(author=name, text=text, post_id=id)
            return redirect("blog:show_post", id=id)

        return Http404("404 Not Found")

    @staticmethod
    def post_new(request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect("blog:show_post", id=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

    @staticmethod
    def post_edit(request, id):
        post = get_object_or_404(Post, id=id)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('blog:show_post', id=post.id)
        else:
            form = PostForm(instance=post)
            return render(request, 'blog/post_edit.html', {'form': form})
