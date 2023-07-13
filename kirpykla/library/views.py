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
from .forms import BarberReviewForm, UserUpdateForm, ProfileUpdateForm, CreateOrderForm
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



class barber(LoginRequiredMixin, CreateView):
    model = Orders
    success_url = "/myorders/"
    template_name = 'barber.html'
    form_class = CreateOrderForm

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        single_barber = get_object_or_404(Barber, pk=self.kwargs['id'])
        context['barber'] = single_barber
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        single_barber = get_object_or_404(Barber, pk=self.kwargs['id'])
        kwargs['barber'] = single_barber
        kwargs['booker'] = self.request.user
        return kwargs