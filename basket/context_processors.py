
def basket(request):
    """ Variables for basket's total price and number of items in basket for navbar info """

    request.session.setdefault('item', {})
    all_items = request.session['item']
    num_of_items = 0
    for item in all_items:
        num_of_items += all_items[item]['quantity']
    sub_total_price = 0
    for item in all_items:
        sub_total_price += float(all_items[item]['price']) * all_items[item]['quantity']

    return {'total_basket_items': num_of_items, 'sub_total_price': sub_total_price}