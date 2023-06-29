from django.shortcuts import render, get_object_or_404
from .models import Barber
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def barber_list(request):
    paginator = Paginator(Barber.objects.all(), 4)
    page_number = request.GET.get('page')
    paged_barbers = paginator.get_page(page_number)
    context = {
        'barbers': paged_barbers
    }   


    return render(request, 'barbers.html', context=context)

def barber(request, id):
    single_barber = get_object_or_404(Barber, pk=id)
    return render(request, 'barber.html', {'barber': single_barber})

def search(request):
   
    query = request.GET.get('query')
    search_results = Barber.objects.filter(Q(name__icontains=query) | Q(last_name__icontains=query))
    return render(request, 'search.html', {'barbers': search_results, 'query': query})