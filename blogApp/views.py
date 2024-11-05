from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from blogApp.models import Post, Comment, Category
from blogApp.forms import CommentForm, SearchForm, ContactForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.safestring import mark_safe
from django.conf import settings


def blog_index(request):
    post_list = Post.objects.all().order_by("-date_created")
    trending_posts = Post.objects.order_by('-views')[:5]
    paginator = Paginator(post_list, 15)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        "posts": posts,
        'trending_posts': trending_posts,
    }
    return render(request, "blog/index.html", context)


def blog_category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    category_post = Post.objects.filter(categories=category).order_by("-date_created")
    paginator = Paginator(category_post, 15)
    category_number = request.GET.get('page')
    posts = paginator.get_page(category_number)
    context = {
        "category": category.name,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    post.increment_views()
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                comment=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(mark_safe(request.path_info))

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),

    }

    return render(request, "blog/detail.html", context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_post = Post.objects.filter(title__icontains=query).order_by("-date_created")
            paginator = Paginator(search_post, 15)
            search_number = request.GET.get('page')
            try:
                results = paginator.get_page(search_number)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
    context = {
        'form': form,
        'query': query,
        'results': results
    }
    return render(request, 'blog/post_search.html', context)


def about_us(request):
    return render(request, 'blog/about_us.html', )


def terms_of_service(request):
    return render(request, 'blog/terms_of_service.html', )


def privacy(request):
    return render(request,'blog/privacy.html',)


def contact_us(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            message = contact_form.cleaned_data['message']

            send_mail(subject=f"New Contact from {name}",
                      message=f"Message from {name} ({email}):\n\n{message}",
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=['nwachukwuclinton2@gmail.com'],
                      fail_silently=False,
                      )
        return render(request, 'blog/contact_us.html')
    else:
        form = ContactForm()
    return render(request, 'blog/contact_us.html', {"form": form})
