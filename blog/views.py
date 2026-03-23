from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.decorators.http import require_POST
from .forms import CommentForm, SearchForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count, Q

def post_list(request,tag_slug=None):
	post_list  = Post.published.all()
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug = tag_slug)
		post_list = post_list .filter(tags__in = [tag])
	paginator = Paginator(post_list , 3)
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
		{'posts': posts,
			'tag': tag,}
		)

def post_search(request):
	form = SearchForm()
	query = None
	results = []

	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			results = Post.published.filter(
				Q(title__icontains=query) | Q(body__icontains=query)
			)

	return render(
		request,
		'blog/post/search.html',
		{
			'form': form,
			'query': query,
			'results': results,
		}
	)
# Create your views here.

def post_detail(request, year, month, day, post):
	post = get_object_or_404(
		Post.published,
		slug = post,
		publish__year = year,
		publish__month = month,
		publish__day = day
		)
	comments = post.comments.filter(active = True)
	form = CommentForm()
	post_tags_ids = post.tags.values_list('id', flat = True)
	similar_posts = Post.published.filter(tags__in = post_tags_ids).exclude(id = post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')
	return render(
		request,
		'blog/post/detail.html',
		{'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts}
		)


@require_POST
def post_comment(request, post_id):
	post = get_object_or_404(Post.published, id = post_id)
	comment = None

	form = CommentForm(data = request.POST)
	if form.is_valid():
		comment = form.save(commit = False)
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
