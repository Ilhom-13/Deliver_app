from food.models import Restaurant, Category


def all_restaurants_categories(request):

    """ Variables for navigation bar dropdown menu """

    restaurants = Restaurant.objects.all()
    category_names = list({category.name for category in Category.objects.all()})
    return {'all_restaurants': restaurants, 'all_category_names': category_names}
