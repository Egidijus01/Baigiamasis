import datetime
import json
import random
from django.forms import TextInput
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.urls import reverse
from .models import Barber, Posts, Services
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import BarberReviewForm, UserUpdateForm, ProfileUpdateForm, BarberForm, PostForm, ServiceForm, ChatMessageForm
from .models import ChatMessage ,Profile, Rating, Orders, ChatRoom, Message, BarberTimeSlotAvailability, Friends
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
                    user = User.objects.create_user(username=username, email=email, password=password)
                    
                    # Create the associated profile
                    profile = user.profile
                    
                    # Optionally create additional related objects
                    Friends.objects.create(profile=profile)

                    
                    messages.info(request, f'Vartotojas "{username}" sekmingai uzregistruotas') # type: ignore
                    return redirect('index')

            

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


def mydata_all(request):
    result_list = list(Barber.objects
                
                .values('id',
                        'name', 
                        'last_name',
                        'city',
                        'country',
                        'adress'
                        ))
  
    return JsonResponse(result_list, safe=False)

def mydata(request, pk):

    result_list = list(Barber.objects.filter(id=pk)
                
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




@login_required
def loaned_orders_for_barber(request):
   
    orders = Orders.objects.filter(barber=request.user.barber).order_by('time_ordered')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    return render(request, 'barber_orders.html', {'orders': page_obj})


@login_required
def order_by_user_detail_view_for_barber(request, pk):
    order = get_object_or_404(Orders, pk=pk, barber=request.user.barber)
    return render(request, 'barber_order.html', {'order': order})


@login_required
def loaned_orders_by_user_list_view(request):
    orders = Orders.objects.filter(booker=request.user).order_by('time_ordered')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    return render(request, 'user_orders.html', {'orders': page_obj})



@login_required
def order_by_user_detail_view(request, pk):
    order = get_object_or_404(Orders, pk=pk, booker=request.user)
    return render(request, 'user_order.html', {'order': order})



import logging

logger = logging.getLogger(__name__)

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
    

    key = settings.GOOGLE_API_KEY
    
    stars = range(1, 6)

    context = {
        
        'key':key,
        'barber': single_barber,
        'form': form,
        'services': single_barber.services.all(),
        'stars':stars
    }


    return render(request, 'barber.html', context=context)


def booking(request, id):
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)
    barber = get_object_or_404(Barber, pk=id)
    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    services = barber.services.all()

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

    print(services)

    return render(request, 'booking.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
            'barber': barber,
            'services': services
        })

def bookingSubmit(request, id):
    barber = get_object_or_404(Barber, pk=id)
    user = request.user
    times = [
        "3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    # Get stored data from Django session
    day = request.session.get('day')
    service = request.session.get('service')

    # Only show the time of the day that is available for the specific barber
    hour = checkTime(times, day, barber)

    # service_instance = None
    # if service:
    #     services_of_barber = 
    #     if services_of_barber.exists():
    #         service_instance = services_of_barber.first()
    service_instance = None
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service is not None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
                    if Orders.objects.filter(day=day).count() < 11:
                        if Orders.objects.filter(barber=barber, day=day, time=time).count() < 1:
                            # Create the order
                            service_instance_qs = barber.services.filter(service_name=service)
                            if service_instance_qs.exists():
                                service_instance = service_instance_qs.first()
                            appointment = Orders.objects.create(
                                booker=user,
                                barber=barber,
                                service=service_instance,
                                day=day,
                                time=time,
                            )
                            # Mark the time slot as unavailable for the specific barber
                            BarberTimeSlotAvailability.objects.create(
                                barber=barber,
                                day=day,
                                time=time,
                                is_available=False,
                            )
                            messages.success(request, "Order Saved!")
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
        'times': hour,
        'barber': barber,
    })




def checkTime(times, day, barber):
    # Only show the time of the day that is available for the specific barber
    x = []
    for k in times:
        if not Orders.objects.filter(barber=barber, day=day, time=k).exists():
            x.append(k)
    return x

def checkEditTime(times, day, barber, id):
    # Only show the time of the day that is available or matches the edited order's time for the specific barber
    x = []
    order = Orders.objects.get(pk=id)
    time = order.time
    for k in times:
        if not BarberTimeSlotAvailability.objects.filter(barber=barber, day=day, time=k, is_available=False).exists() or time == k:
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


def get_available_times(barber, day):
    available_times = BarberTimeSlotAvailability.objects.filter(barber=barber, day=day, is_available=True)
    return available_times



@login_required
def chat_room_list(request):
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'chat.html', {'chat_rooms': chat_rooms})

def room(request, room_name):
  username = request.GET.get('username', 'Anonymous')
    
  return render(request, 'room.html', {'room_name': room_name, 'username': username})


def become_barber(request):
    user = request.user
 


    if request.method == 'POST':
        form = BarberForm(request.POST, request.FILES)
        if form.is_valid():
            Barber.objects.create(
                user = user,
                name = form.cleaned_data['name'],
                last_name = form.cleaned_data['last_name'],
                email = user.email,
                about = form.cleaned_data['about'],
                login_name = user.username,
                zipcode = form.cleaned_data['zipcode'],
                city = form.cleaned_data['city'],
                country = form.cleaned_data['country'],
                adress = form.cleaned_data['adress'],
                group = Group.objects.get(name='kirpejai'),
                cover = form.cleaned_data['cover']
            )
            kirpejai_group = Group.objects.get(name='kirpejai')
            user.groups.add(kirpejai_group)
            
            
            return redirect('barbers')  # Redirect to the list view after successfully creating the Barber object
    else:
        form = BarberForm()
    return render(request, 'become_barber.html', {'form': form})




def my_posts(request, id):
    user = get_object_or_404(User, pk=id)
    
    posts = Posts.objects.filter(author=request.user.barber)
    posts_per_page = 5
    paginator = Paginator(posts, posts_per_page)

    # Get the requested page number from the URL
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    


    return render(request, 'my_posts.html', {
            
            'posts':page_obj,
            'barber': user,
        })

def create_post(request, id):
    user = get_object_or_404(User, pk=id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = user.barber
            post.save()
            return redirect('my_posts', id=user.id) # type: ignore
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})
        

def update_post(request, id):
    post = get_object_or_404(Posts, pk=id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect('my_posts', id=post.author.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'update_post.html', {'form': form})


def delete_post(request, id):
    post = get_object_or_404(Posts, pk=id)

    if request.method == 'POST':
        post.delete()
        return redirect('my_posts', id=post.author.id)

    # If the request method is not POST, render the template to confirm the deletion
    return render(request, 'delete_post.html', {'post': post})


def get_paginated_data(request):
    data_list = Posts.objects.all()
    data_list = list(data_list)  # Convert the queryset to a list
    random.shuffle(data_list)   # Randomly shuffle the list
    paginator = Paginator(data_list, 10)
    page_number = request.GET.get('page')
    data_page = paginator.get_page(page_number)

    return render(request, 'posts_partial.html', {'data_page': data_page})


def explore(request):
    return render(request, 'explore.html')


def update_barber_page(request):
    if request.method == 'POST':
        form = BarberForm(request.POST, request.FILES, instance=request.user.barber)
        if form.is_valid():
            form.save()
            return redirect('barber_profile')
    else:
        form = BarberForm(instance=request.user.barber)


    context = {
        'form': form,
    }

    return render(request, 'edit_barber_profile.html', context=context)


def add_prices(request):
    barber = request.user.barber
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()

            barber.services.add(service)
            return redirect('add_prices')
    else:
        form = ServiceForm()

    services = barber.services.all()

    context = {'form': form,
               'services': services}

    return render(request, 'add_prices.html', context=context)


def testukas(request):
    user = request.user
    friends = user.profile.friends.all()

    context = {
        'user': user,
        'friends': friends,
    }

    return render(request, 'testaas.html', context)

@login_required
def testas_detail(request, pk):
    friend = Friends.objects.get(profile_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.profile.id)
    chats = ChatMessage.objects.all()
    rec_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    rec_chats.update(seen=True)
    
    form = ChatMessageForm()

    if request.method == "POST":
        
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect('testas_detail', pk=friend.profile.id)

    context = { 'friend': friend,
               'form': form,
               'user':user,
               'profile':profile,
               'chats':chats,
               'num': rec_chats.count()
               }
    return render(request ,'testas_detail.html', context)

def sentMessages(request, pk):
    friend = Friends.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    user = request.user.profile
    data = json.loads(request.body)
    new_chat = data['msg']
    new_chat_message = ChatMessage.objects.create(
        body=new_chat,
        msg_sender = user,
        msg_receiver = profile,
        seen=False
        )
    print(new_chat)
    return JsonResponse(new_chat_message.body, safe=False)


def receivedMessages(request, pk):
    friend = Friends.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    user = request.user.profile
    arr = []
    
    chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    for chat in chats:
        arr.append(chat.body)

    return JsonResponse(arr, safe=False)


def chatNotification(request):
    user = request.user.profile
    friends = user.friends.all()
    arr = []
    for friend in friends:
        chats = ChatMessage.objects.filter(msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)
        arr.append(chats.count())
    
    return JsonResponse(arr, safe=False)

def add_friend(request, pk):
    user_profile = request.user.profile
    
    try:
        barber = Barber.objects.get(id=pk)
    except Barber.DoesNotExist:
        return HttpResponse("Barber not found")
    
    real_user_profile = barber.user.profile
    
    # Create a Friends instance for the real_user_profile
    friends_instance = Friends.objects.get(profile=real_user_profile)
    user_friends_inst = Friends.objects.get(profile=user_profile)
    
    # Add the Friends instance to the user_profile's friends
    user_profile.friends.add(friends_instance)
    real_user_profile.friends.add(user_friends_inst)
    
    return redirect('index') 