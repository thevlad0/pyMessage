from django.http import JsonResponse

# Create your views here.
def search_users(request, filter_text=None):
    found_users = request.user.search(filter_text)
    return JsonResponse(found_users, safe=False)