from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
        )
# Create your views here.

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post.published,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request,
        'blog/post/detail.html',
        {'post': post, 'comments': comments, 'form': form}
        )

@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Post.published, id=post_id)
    comment = None

    form = CommentForm(data = request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )