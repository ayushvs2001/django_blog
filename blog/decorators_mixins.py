from django.http import HttpResponse
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def check_admin(request, *args, **kwargs):
    return request.user.is_staff or request.user.is_superuser


# only admin mixin
# it take check_group function if it is admin then proceed futher to the original function
# if current user is not admin then it is redirect to home
class OnlyAdmin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return check_admin(self.request)

# this mixin check whether the user which tries to delete the post
# is admin or author of this commment
class DeleteCommentMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
       return (str(self.request.user) == str(self.get_object().author)) or check_admin(self.request)


# only admin decorator
# it take check_group function if it is admin then proceed futher to the original function
# if current user is not admin then it is redirect to home
def only_admin(view_func):
    def wrapper_func(request, *args, **kwargs):

        if check_admin(request, *args, **kwargs):
           return view_func(request, *args, **kwargs)
        else:
           return redirect('home')

    return wrapper_func
