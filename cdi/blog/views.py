from django.http import Http404

from .models import BlogModel, CommentModel
from .forms import CommentForm, SearchForm, SectionSearch
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from main.models import Section


def blog_list_view(request):
    dataset = BlogModel.objects.all()
    sections = Section.objects.all()
    recent_posts = BlogModel.objects.all()[:3]
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            titleBlog = form.cleaned_data['titleBlog']
            dataset = BlogModel.objects.filter(blog_title__icontains=form['titleBlog'].value())
    else:
        form = SearchForm()

    if request.method == 'GET' and 'section' in request.GET:
        section_search = SectionSearch(request.GET)
        section = section_search['section'].value()
        dataset = BlogModel.objects.filter(section_id=section)
    else:
        section_search = SectionSearch()
    paginator = Paginator(dataset, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Blog',
        'sections': sections,
        'page_obj': page_obj,
        'recent_posts': recent_posts,
        'form': form,
    }
    return render(request, 'blog/listview.html', context)


def blog_detail_view(request, _id):
    try:
        data = BlogModel.objects.get(id=_id)
        comments = CommentModel.objects.filter(blog=data)
        sections = Section.objects.all()
        recent_posts = BlogModel.objects.all()[:3]
    except BlogModel.DoesNotExist:
        raise Http404('Data does not exist')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = CommentModel(your_name=form.cleaned_data['your_name'],
                                   your_email=form.cleaned_data['your_email'],
                                   comment_text=form.cleaned_data['comment_text'],
                                   blog=data)
            comment.save()
            return redirect(f'/blogs/{_id}')
    else:
        form = CommentForm()

    context = {
        'title': 'Blog Detail',
        'subtitle': f'Blog: {_id}',
        'data': data,
        'form': form,
        'sections': sections,
        'recent_posts': recent_posts,
        'comments': comments,
        'class': 'single-post-area'
    }
    return render(request, 'blog/detailview.html', context)
