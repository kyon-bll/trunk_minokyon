from django.views import generic


class MinonoIndexView(generic.TemplateView):
    template_name = 'minono/minono.html'


class MinonoPointView(generic.TemplateView):
    template_name = 'minono/point.html'
