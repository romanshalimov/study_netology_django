from django.http import HttpResponse
from django.shortcuts import render, reverse
from datetime import datetime
import os

def home_view(request):
    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir'),
    }
    context = {
        'pages': pages
    }
    return render(request, template_name, context)

def time_view(request):
    current_time = datetime.now().time().strftime('%H:%M')
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)

def workdir_view(request):
    workdir_list = '<br>'.join(os.listdir(path='.'))
    msg = f'Содержимое рабочей директории:<br>{workdir_list}'
    return HttpResponse(msg)