from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class TestHomeView(View):
    def get(self, request):
        return HttpResponse('<html><head><title>Home</title></head><body><p>Welcome!</p></body></html>')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TestHomeView, self).dispatch(*args, **kwargs)
