from django.shortcuts import render, get_object_or_404

def home(request):
    content = {}
    return render(request, 'home.html', content)