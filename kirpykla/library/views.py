import datetime
from django.forms import TextInput
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Barber
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import BarberReviewForm, UserUpdateForm, ProfileUpdateForm
from .models import Rating, Orders
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from datetime import timedelta


# Create your views here.
from django.http import HttpResponse, JsonResponse

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

# def barber(request, id):
#     single_barber = get_object_or_404(Barber, pk=id)


#     return render(request,"barber.html",{"barber": single_barber, })#"form": form
    # if request.method == 'POST':        
    #     form = BarberReviewForm(request.POST)        
    #     if form.is_valid():            
    #         Rating.objects.create(             
    #             barber = single_barber,                
    #             reviewer = request.user,          
    #             content = form.cleaned_data['content'],
    #             rating = form.cleaned_data['rating']
    #             )            
    #         return redirect('barber', id=id)

    # form = BarberReviewForm()
           
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
            if User.objects.filter(username=username).exists(): # type: ignore
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

def map_settings(request):
    return render(request, 'settings.html')

def map(request):
    key = settings.GOOGLE_API_KEY
    context = {
        'key':key,
    }
    return render(request, 'map.html',context)

def mydata(request):
    result_list = list(Barber.objects\
                
                .values('id',
                        'name', 
                        'last_name',
                        'city',
                        'country',
                        'adress'
                        ))
  
    return JsonResponse(result_list, safe=False)

@login_required
def profile(request):
    if request.method=='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context=context)




class LoanedOrdersByUserListView(LoginRequiredMixin, ListView):
    model = Orders
    context_object_name = 'orders'
    template_name = 'user_orders.html'
    paginate_by = 10

    def get_queryset(self):
        return Orders.objects.filter(booker=self.request.user).order_by('time_ordered') # type: ignore


class OrderByUserDetailView(LoginRequiredMixin, DetailView):
    model = Orders
    template_name = 'user_order.html'




import logging

logger = logging.getLogger(__name__)

def barber(request, id):
    single_barber = get_object_or_404(Barber, pk=id)
    
    if request.method=='POST':
        
        pass
    

    context = {
        
        
        'barber': single_barber
    }

    return render(request, 'barber.html', context=context)


def booking(request, id):
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)
    barber = get_object_or_404(Barber, pk=id)
    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        if service == None:
            messages.success(request, "Please Select A Service!")
            return redirect('booking', id=id)

        #Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service

        return redirect('bookingSubmit', id=id)


    return render(request, 'booking.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
            'barber': barber,
        })

def bookingSubmit(request, id):
    barber = barber = get_object_or_404(Barber, pk=id)
    user = request.user
    times = [
        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    #Get stored data from django session:
    day = request.session.get('day')
    service = request.session.get('service')
    
    #Only show the time of the day that has not been selected before:
    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
                    if Orders.objects.filter(day=day).count() < 11:
                        if Orders.objects.filter(day=day, time=time).count() < 1:
                            AppointmentForm = Orders.objects.get_or_create(
                                booker = user,
                                barber = barber,
                                service = service,
                                day = day,
                                time = time,
                            )
                            
                            messages.success(request, "Orders Saved!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")


    return render(request, 'booking-submit.html', {
        'times':hour,
        'barber': barber,
    })


def checkTime(times, day):
    #Only show the time of the day that has not been selected before:
    x = []
    for k in times:
        if Orders.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x

def checkEditTime(times, day, id):
    #Only show the time of the day that has not been selected before:
    x = []
    order = Orders.objects.get(pk=id)
    time = order.time
    for k in times:
        if Orders.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x


def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Orders.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays

def dayToWeekday(x):
    z = datetime.datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y

def validWeekday(days):
    #Loop days you want in the next 21 days:
    today = datetime.datetime.now()
    weekdays = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Monday' or y == 'Saturday' or y == 'Wednesday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays



def chat(request):
    return render(request, 'chat.html')


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })