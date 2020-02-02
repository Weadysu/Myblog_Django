from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from read_statistics.models import ReadNum
from read_statistics.utils import read_statistics_once_read

# Create your views here.

def get_blog_list_common_data(request, blogs_list):
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

    # Obtain corresponding numbers of different date archive
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                        created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    content = {}
    content['blogs'] = page_of_blogs.object_list
    content['page_range'] = page_range
    content['page_of_blogs'] = page_of_blogs
    content['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    content['blog_dates'] = blog_dates_dict

    return content

def blog_list(request):
    blogs_list = Blog.objects.all()
    content = get_blog_list_common_data(request, blogs_list)
    return render(request, 'blog/blog_list.html', content)

def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_list = Blog.objects.filter(blog_type=blog_type)
    content = get_blog_list_common_data(request, blogs_list)
    content['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', content)

def blogs_with_date(request, year, month):
    blogs_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    content = get_blog_list_common_data(request, blogs_list)
    content['blog_date'] = '%s/%s' % (month, year)
    return render(request, 'blog/blogs_with_date.html', content)

def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)

    content = {} 
    content['blog'] = blog
    content['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    content['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    response = render(request, 'blog/blog_detail.html', content)
    response.set_cookie(read_cookie_key, 'True') # readed_cookie_tag
    return response