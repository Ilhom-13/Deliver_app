from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from food.models import Item


@login_required
def basket_summary(request):
    basket_info = {int(id_): value['quantity'] for id_, value in request.session['item'].items()}
    items = {}
    for id_ in basket_info:
        item = items[id_] = Item.objects.get(id=id_)
        total_price = item.price * basket_info[id_]
        item.total_price = total_price
        item.quantity = basket_info[id_]
        item.save()
    else:
        context = {'items': items}
        return render(request, 'basket/basket_summary.html', context)


@login_required
def basket_add(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(Item, id=pk)
        basket = request.session.get('item', {})
        pk = str(pk)
        if pk not in basket:
            basket[pk] = {'price': str(item.price)}
            basket[pk]['quantity'] = 1
        else:
            basket[pk]['quantity'] += 1
        request.session.modified = True
        return redirect('basket:basket-summary')


@login_required
def basket_delete(request, pk):
    if request.method == 'POST':
        pk = str(pk)
        item = request.session['item'][pk]
        item['quantity'] -= 1
        if item['quantity'] <= 0:
            del request.session['item'][pk]
        request.session.modified = True
        return redirect('basket:basket-summary')
