from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.conf import settings

# Create your views here.
num_of_blogs_per_page = 2

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list, settings.NUM_OF_BLOGS_PER_PAGE)
    page_num = request.GET.get('page', 1) # Get page parameter(GET request)
    page_of_blogs = paginator.get_page(page_num)
    current = page_of_blogs.number # Get current page number
    page_range = [x for x in range(current-2, current+3) if (x >= 1 and x <= paginator.num_pages)] # Get pages within 2 of distance of current page 

    # Add Ellipsis
    if page_range[0] >= 3:
        page_range.insert(0, '...')
    if page_range[-1] <= paginator.num_pages - 2:
        page_range.insert(paginator.num_pages, '...')

    # Add first and last page
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.insert(paginator.num_pages, paginator.num_pages)

    content = {}
    content['page_range'] = page_range
    content['blogs'] = page_of_blogs.object_list
    content['page_of_blogs'] = page_of_blogs
    content['blog_types'] = BlogType.objects.all()
    return render(request, 'blog/blog_list.html', content)

def blog_detail(request, blog_pk):
    content = {}
    content['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blog/blog_detail.html', content)

def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_list = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs_list, settings.NUM_OF_BLOGS_PER_PAGE)
    page_num = request.GET.get('page', 1) # Get page parameter(GET request)
    page_of_blogs = paginator.get_page(page_num)
    current = page_of_blogs.number # Get current page number
    page_range = [x for x in range(current-2, current+3) if (x >= 1 and x <= paginator.num_pages)] # Get pages within 2 of distance of current page 

    # Add Ellipsis
    if page_range[0] >= 3:
        page_range.insert(0, '...')
    if page_range[-1] <= paginator.num_pages - 2:
        page_range.insert(paginator.num_pages, '...')

    # Add first and last page
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.insert(paginator.num_pages, paginator.num_pages)

    content = {}
    content['page_range'] = page_range
    content['blogs'] = page_of_blogs.object_list
    content['page_of_blogs'] = page_of_blogs
    content['blog_types'] = BlogType.objects.all()
    content['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', content)