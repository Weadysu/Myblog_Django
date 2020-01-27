from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator

# Create your views here.

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list, 10) # 10 items per page
    page_num = request.GET.get('page', 1) # Get page parameter(GET request)
    page_of_blogs = paginator.get_page(page_num)
    
    content = {}
    content['page_of_blogs'] = page_of_blogs
    content['blog_types'] = BlogType.objects.all()
    return render(request, 'blog/blog_list.html', content)

def blog_detail(request, blog_pk):
    content = {}
    content['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blog/blog_detail.html', content)

def blogs_with_type(request, blog_type_pk):
    content = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    content['blog_type'] = blog_type
    content['blogs'] = Blog.objects.filter(blog_type=blog_type)
    content['blog_types'] = BlogType.objects.all()
    return render(request, 'blog/blogs_with_type.html', content)