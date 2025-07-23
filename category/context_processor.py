from .models import Category
def all_category(request): 
    all_category_links = Category.objects.all()
    return {'all_category_links': all_category_links}