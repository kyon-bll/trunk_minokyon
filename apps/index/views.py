from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model

from progress.services import get_user_statuses
from .utils import get_course_step_list
from .contexts import Panel, today_overdue_status_str

from clients.forms import ClientAddForm, ClientStaffAddForm
from clients.services import (
    create_client_staff_from_property, create_client_with_blank_staff)
from clients.contexts import ClientAddModal, ClientStaffAddModal

from projects.forms import ProjectForm
from progress.utils import create_project_shortcut
from progress.contexts import ProjectCreateModalContext

from gas_calendar.utils import get_steps_todo_today

from extra_views.multiformviews import MultiFormsView


class IndexView(MultiFormsView):
    template_name = 'index/index.html'

    is_index = True
    title = 'ホーム'

    @property
    def info(self):
        return today_overdue_status_str(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        self.statuses = get_user_statuses(request.user)
        return super().dispatch(request, *args, **kwargs)

    # multiform
    form_classes = dict(
        client=ClientAddForm,
        client_staff=ClientStaffAddForm,
        project=ProjectForm)
    success_url = reverse_lazy('index:index')

    def get_form_kwargs(self, form_name, bind_form=False):
        kwargs = super(IndexView, self).get_form_kwargs(form_name, bind_form)
        if form_name == 'client_staff':
            kwargs['clients'] = self.request.user.groups.get().clients.all()
        if form_name == 'project':
            kwargs['user'] = self.request.user
        return kwargs

    def client_staff_form_valid(self, form):
        client = form.cleaned_data['client']
        staff_property = form.save(commit=False)
        create_client_staff_from_property(self.request, client, staff_property)
        return redirect(self.success_url)

    def client_form_valid(self, form):
        client = form.save(commit=False)
        client.auth_group = self.request.user.groups.get()
        create_client_with_blank_staff(self.request, client)
        return redirect(self.success_url)

    def project_form_valid(self, form):
        project = form.save(commit=False)
        project_members = get_user_model().objects.filter(
            id__in=form['project_members'].value())
        create_project_shortcut(self.request, project, project_members)
        return redirect(self.success_url)

    def forms_invalid(self, forms, form_name):
        if form_name == 'client_staff':
            messages.warning(self.request, '取引先従業員を追加できませんでした。')
        if form_name == 'client':
            messages.warning(self.request, '取引先を追加できませんでした。')
        if form_name == 'project':
            messages.warning(self.request, '案件を作成できませんでした。')
        return super().forms_invalid(forms, form_name)

    # context
    panel_border_list = [
        'border-right border-bottom',
        'border-right border-bottom',
        'border-bottom',
        'border-right',
        'border-right',
        '']

    @property
    def panel_list(self):
        steps_tuple = get_steps_todo_today(self.request.user)
        steps = steps_tuple[0]+steps_tuple[1]
        course_step_list = get_course_step_list(steps)
        panel_list = [
            Panel(course_steps, 23, 27) for course_steps in course_step_list]
        n = len(panel_list)
        for i in range(6-n):
            panel_list.append(Panel())
        return panel_list

    quick_access_list = [
        ('client', ClientAddModal),
        ('client_staff', ClientStaffAddModal),
        ('project', ProjectCreateModalContext)]

    @property
    def quick_access_context_list(self):
        context_list = [
            self.get_quick_access_context(*q) for q in self.quick_access_list]
        return context_list

    def get_quick_access_context(self, form_name, context_class):
        if form_name == self.request.POST.get('action'):
            form = self.get_forms(self.form_classes, (form_name,)).get(form_name)
        else:
            form = self.get_forms(self.form_classes).get(form_name)
        modal_context = context_class(form)
        modal_context.content.submit_name = 'action'
        modal_context.content.submit_value = form_name
        return {'modal': modal_context}
