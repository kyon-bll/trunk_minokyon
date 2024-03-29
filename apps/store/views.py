from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm


from .models import StoreLog


class StoreIndexView(generic.TemplateView):
    template_name = 'store/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        if 'username' in request.GET:
            s = StoreLog(
                store_user=request.user,
                username=request.GET.get('username'),
                kind=request.GET.get('kind'),
                geek_rank=request.GET.get('rank'),
                created_at=request.GET.get('date'))
            s.save()
            return redirect('store:index')

        return super().get(request, *args, **kwargs)


class StoreUserRegistView(generic.CreateView):
    template_name = 'store/regist.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('store:index')
