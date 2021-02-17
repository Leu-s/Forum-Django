from django.shortcuts import render
from django.shortcuts import HttpResponse


def main_page(request):
    return render(request, 'articles/main_page.html')
