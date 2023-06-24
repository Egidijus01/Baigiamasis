from django.shortcuts import render, get_object_or_404
from .models import Barber


# Create your views here.
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def barber_list(request):
    context = {'barbers': Barber.objects.all()}
    return render(request, 'barbers.html', context=context)

def barber(request, id):
    single_barber = get_object_or_404(Barber, pk=id)
    return render(request, 'barber.html', {'barber': single_barber})