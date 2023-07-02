from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Barber
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import BarberReviewForm
from .models import Rating

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

    if request.method == 'POST':        
        form = BarberReviewForm(request.POST)        
        if form.is_valid():            
            Rating.objects.create(             
                barber = single_barber,                
                reviewer = request.user,          
                content = form.cleaned_data['content'],
                rating = form.cleaned_data['rating']
                )            
            return redirect('barber', id=id)

    form = BarberReviewForm()
           
    return render(request,"barber.html",{"barber": single_barber, "form": form})

def search(request):
   
    query = request.GET.get('query')
    search_results = Barber.objects.filter(Q(name__icontains=query) | Q(last_name__icontains=query))




    return render(request, 'search.html', {'barbers': search_results, 'query': query})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                print('uzimtas')
                messages.error(request, f'Vartotojo vardas "{username}" jau uzimtas')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojo email "{email}" jau uzimtas')

                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)

                    
                    messages.info(request, f'Vartotojas "{username}" sekmingai uzregistruotas')
                    return redirect('login')

            

        else:

            messages.error(request, 'Slaptazodziai nesutampa')
            return redirect('register')
    return render(request, 'register.html')