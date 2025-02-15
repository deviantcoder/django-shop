from .models import Category


def categories(request):
    """
    Context processor that retrieves all top-level categories.
    """

    categories = Category.objects.filter(parent=None)
    return {'categories': categories}