from .models import StoreProfile

def store_context(request):
    store_name = ''
    if getattr(request, 'user', None) and request.user.is_authenticated:
        try:
            sp = request.user.store_profile
            store_name = getattr(sp, 'store_name', '')
        except StoreProfile.DoesNotExist:
            store_name = ''
    return {'store_name': store_name}
