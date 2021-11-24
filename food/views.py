from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from users.models import NewUser
from .models import Item, Restaurant, Category, Order
from .forms import ItemCreationForm, CategoryCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import date
from django.urls import reverse


class HomeView(ListView):
    template_name = 'food/index.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['category_names'] = list({category.name for category in Category.objects.all()
                                          if Item.objects.filter(category__name=category.name).exists()})
        context['categories'] = Category.objects.all()
        return context


class ItemListView(ListView):
    """List of all items to make an order """

    template_name = 'food/all_items.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.all().order_by('price')


class ItemDetail(DetailView):
    template_name = 'food/item.html'
    context_object_name = 'item'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Item.objects.all()


class CategoryView(ListView):
    template_name = 'food/category.html'
    context_object_name = 'items'

    def get_queryset(self):
        category = Category.objects.filter(name__iexact=(self.kwargs['category'])).first()
        return Item.objects.filter(category__name__iexact=category.name)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category = Category.objects.filter(name__iexact=self.kwargs['category']).first()
        context['category'] = category
        restaurant_names = [res.name for res in Restaurant.objects.all()]
        users = NewUser.objects.all()
        res_users = [user for user in users if user.user_name in restaurant_names and
                     Item.objects.filter(owner__name=user.user_name).
                     filter(category__name__iexact=(self.kwargs['category'])).exists()]
        context['restaurants'] = res_users
        return context


class RestaurantView(ListView):
    template_name = 'food/restaurant.html'
    context_object_name = 'items'

    def get_queryset(self):
        restaurant = Restaurant.objects.get(slug=self.kwargs['slug'])
        return Item.objects.filter(owner=restaurant)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        restaurant = Restaurant.objects.get(slug=self.kwargs['slug'])
        context['restaurant'] = restaurant
        context['categories'] = Category.objects.filter(user__user_name=restaurant.name)
        return context


class RestaurantSellInfoView(UserPassesTestMixin, ListView):
    """ This view is only for restaurant users.
        They can see items info about times of sold  """

    def test_func(self):
        return self.request.user.groups.filter(name='Restaurants').exists()

    def handle_no_permission(self):
        return JsonResponse({'message': 'Only restaurants can access this view'})

    template_name = 'food/restaurant_sell_info.html'
    context_object_name = 'items'

    def get_queryset(self):
        restaurant = Restaurant.objects.get(slug=self.kwargs['slug'])
        return Item.objects.filter(owner=restaurant).order_by('-num_of_sold')


def user_in_restaurant_group(user):
    if user:
        return user.groups.filter(name='Restaurants').exists()


today = {
         'year': int(date.today().strftime('%Y')),
         'month': date.today().strftime('%b'),
         'day': date.today().strftime('%d')
        }


@user_passes_test(user_in_restaurant_group, login_url='food:home')
def item_create(request):

    """ Only restaurant users can create item """

    if request.method == 'POST':
        form = ItemCreationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            category = form.cleaned_data['category']
            image = form.cleaned_data['image']
            restaurant = Restaurant.objects.get(name=request.user.user_name)
            item = Item(name=name, price=price, category=category, image=image, owner=restaurant)
            item.slug = slugify(name)
            item.save()
            return redirect(reverse('accounts:dashboard', kwargs={**today}))
        return render(request, 'food/add_item.html', {'form': form})

    """ Pass user to a form to assign item's category
     from categories that user created and not others """

    form = ItemCreationForm(user=request.user)
    return render(request, 'food/add_item.html', {'form': form})


@user_passes_test(user_in_restaurant_group, login_url='food:home')
def item_delete(request, pk):

    """ Only restaurant users can create item """

    if request.method == 'POST':
        item = Item.objects.get(id=pk)
        if item.owner.name == request.user.user_name:
            for order in Order.objects.all():
                order.items.remove(item)
                if order.items.all().count() <= 0:
                    order.delete()
            item.delete()
            return redirect(reverse('food:items-for-deletion'))
        else:
            return JsonResponse({
                'message': 'You have no authority to delete this item'
            })
    else:
        return redirect('food:items-for-deletion')


class ItemsDeletionView(UserPassesTestMixin, ListView):

    def test_func(self):
        return self.request.user.groups.filter(name='Restaurants').exists()

    def handle_no_permission(self):
        return JsonResponse({'message': 'Only restaurants can access this view'})

    template_name = 'food/items_deletion.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.filter(owner__name=self.request.user.user_name)



@user_passes_test(user_in_restaurant_group, login_url='food:home')
def category_create(request):
    if request.method == 'POST':
        form = CategoryCreationForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect(reverse('accounts:dashboard', kwargs={**today}))
        return render(request, 'food/category_add.html', {'form': form})
    form = CategoryCreationForm()
    return render(request, 'food/category_add.html', {'form': form})


@login_required
def order_update(request, pk):
    """
    If restaurant clicks ready button order status changes from preparing to delivering.
    If orderer takes his order and clicks ready button, order is done and for each item
    in order increase num of sold time
    """
    order = Order.objects.get(pk=pk)
    if request.user.groups.filter(name='Restaurants').exists():
        owners = [item.owner.name for item in order.items.all()]
        if request.method == 'POST':
            if request.user.user_name in owners:
                if 'ready' in request.POST:
                    order.status = 'delivering'
                    order.save()
                if 'cancel' in request.POST:
                    order.delete()
                return redirect(reverse('accounts:dashboard', kwargs={**today}))
    else:
        if request.method == 'POST':
            if order.user == request.user:
                if 'ready' in request.POST:
                    order.status = 'done'
                    items = order.items.all()
                    for item in items:
                        item.num_of_sold += item.quantity
                        item.save()
                    else:
                        order.save()

                if 'cancel' in request.POST:
                    order.delete()
                return redirect(reverse('accounts:dashboard', kwargs={**today}))
        return redirect(reverse('accounts:dashboard', kwargs={**today}))


@login_required
def order_create(request):
    if request.method == 'POST':
        basket = request.session['item']
        adress = request.POST.get('adress')
        phone = request.POST.get('phone')
        items_id = [int(id_) for id_ in basket]
        items = [Item.objects.get(id=id_) for id_ in items_id]
        restaurants = {}
        for item in items:
            if item.owner not in restaurants:
                restaurants[item.owner] = {item.id: item}
            else:
                restaurants[item.owner][item.id] = item

        for restaurant in restaurants.values():
            restaurant_items = [item for item in restaurant.values()]
            total_price = sum(map(lambda item_: item_.total_price, restaurant_items))
            order = Order.objects.create(user=request.user, adress=adress, phone=phone, total_price=total_price)
            for item in restaurant_items:
                order.items.add(item)
            order.save()

        request.session['item'] = {}
        request.session.modified = True
        return redirect(reverse('accounts:dashboard', kwargs={**today}))
