
from django.shortcuts import render
from .models import CustomUser
from functools import wraps
from django.http import HttpResponseRedirect,HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.views.static import serve
from django.http import Http404,HttpResponse
from django.contrib.auth.decorators import login_required

from django.views.static import serve

def require_user_type(user_type):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                # Get the current logged-in user
                user = CustomUser.objects.get(id=request.user.id)
                # Check if user has the required user_type
                if str(user.user_type) in str(user_type):
                    return view_func(request, *args, **kwargs)
                else:
                    return render(request,'hr_management/404_not_found.html')
            except:
                return HttpResponseRedirect('/')
        return wrapper
    return decorator


# @login_required
# def protected_media_serve(request, path):
#     user = request.user

#     # Check if the user has the appropriate permissions to access this media file.
#     if user.user_type in ['4', '5', '1']:
#         # Serve the media file.
#         return serve(request, path, document_root=settings.MEDIA_ROOT)
#     elif user.user_type == '3':
#         # Check if the user is the owner of the media file based on the path.
#         if is_user_owner_of_media(user, path):
#             return serve(request, path, document_root=settings.MEDIA_ROOT)
    
#     # Raise a 404 error for unauthorized access.
#     return render(request,'hr_management/access_denied.html')

# def is_user_owner_of_media(user, path):
#     first_name = user.first_name
#     last_name = user.last_name
#     name = f'{first_name}_{last_name}'
#     if name in path:
#         return True
#     return False


