import datetime
from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserLoginForm, RestaurantRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import NewUser, Profile
from django.contrib.auth import login
from django.contrib.auth.models import Group
from food.models import Adress, Restaurant
from django.utils.text import slugify
from django.views.generic import ListView
from django.urls import reverse
from datetime import date
from food.models import Order


def user_register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            name = register_form.cleaned_data['user_name']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = NewUser(user_name=name, email=email)
            user.set_password(password)
            user.is_active = True
            user.save()
            return redirect('accounts:login')
        return render(request, 'users/register.html', {'form': register_form})
    register_form = RegistrationForm()
    return render(request, 'users/register.html', {'form': register_form})


def user_login(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            user = NewUser.objects.filter(email=email).first()
            if user:
                if user.check_password(login_form.cleaned_data['password']):
                    login(request, user)
                    return redirect(reverse('accounts:dashboard', kwargs={
                                                                         'year': int(date.today().strftime('%Y')),
                                                                         'month': date.today().strftime('%b'),
                                                                         'day': date.today().strftime('%d')
                                                                         }))
            return render(request, 'users/login.html', {
                                                        'form': login_form,
                                                        'message': 'Email or Password is wrong. Please, try again'
                                                        })
    else:
        login_form = UserLoginForm()
        return render(request, 'users/login.html', {'form': login_form})


def restaurant_register(request):
    if request.method == 'POST':
        form = RestaurantRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            open_at = form.cleaned_data['open_at']
            close_at = form.cleaned_data['close_at']
            day_off = form.cleaned_data['day_off']
            contact = form.cleaned_data['contact']
            city = form.cleaned_data['city']
            district = form.cleaned_data['district']
            restaurant = Restaurant(name=name, email=email, close_at=close_at,
                                    open_at=open_at, contact=contact, day_off=day_off)
            restaurant.slug = slugify(name)
            restaurant.save()
            address = Adress.objects.create(city=city, district=district, place=restaurant)
            user = NewUser(user_name=name, email=email)
            user.set_password(password)
            user.is_active = True
            user.save()
            restaurant_group = Group.objects.get(name='Restaurants')
            restaurant_group.user_set.add(user)
            return redirect('accounts:login')
        return render(request, 'users/restaurant_register.html', {'form': form})
    form = RestaurantRegisterForm()
    return render(request, 'users/restaurant_register.html', {'form': form})


class DailyDashboardView(LoginRequiredMixin, ListView):
    """
        Show orders daily for users and restaurants accordingly.
        get_context_data takes all dates for user if user has order on that date
    '"""

    template_name = 'users/dashboard.html'
    context_object_name = 'orders'

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        requested_date = datetime.datetime.strptime(f"{year} {month} {day}", '%Y %b %d')
        res_group = Group.objects.get(name='Restaurants')
        if res_group in self.request.user.groups.all():
            return Order.objects.filter(items__owner__name=self.request.user.user_name).\
                                 filter(date__date=requested_date.date()).order_by('-date')

        return Order.objects.filter(user=self.request.user).\
                             filter(date__date=requested_date.date()).order_by('-date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        res_group = Group.objects.get(name='Restaurants')
        if res_group in self.request.user.groups.all():
            context['restaurant'] = Restaurant.objects.get(name=self.request.user.user_name)
            context['dates'] = Order.objects.filter(items__owner__name=self.request.user.user_name).dates('date', 'day')
        else:
            context['dates'] = Order.objects.filter(user=self.request.user).dates('date', 'day')
        return context


@login_required
def profile(request):
    user = request.user
    profile_ = Profile.objects.get(user=user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_)
        if u_form.is_valid():
            if p_form.is_valid():
                u_form.save()
                p_form.save()
                return redirect('accounts:profile')
        context = {
                 'profile': profile_,
                 'u_form': u_form,
                 'p_form': p_form
                }
        return render(request, 'users/profile.html', context)
    u_form = UserUpdateForm(instance=user)
    p_form = ProfileUpdateForm(instance=profile_)
    context = {
                'profile': profile_,
                'u_form': u_form,
                'p_form': p_form
            }
    return render(request, 'users/profile.html', context)
