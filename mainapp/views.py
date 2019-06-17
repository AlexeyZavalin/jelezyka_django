from django.shortcuts import render
from mainapp.models import Slide


# Create your views here.

def index(request):
    slides = Slide.objects.filter(slider__name='Слайдер на главной')
    return render(request, 'mainapp/index.html', {'slides': slides})
