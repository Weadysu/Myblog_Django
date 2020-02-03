from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_reading_data_within_seven_days
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_reading_data_within_seven_days(blog_content_type)

    content = {}
    content['dates'] = dates
    content['read_nums'] = read_nums
    return render(request, 'home.html', content)