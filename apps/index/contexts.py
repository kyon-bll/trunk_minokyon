from datetime import datetime, date, time
from collections import Counter

from django.core.urlresolvers import reverse_lazy

from progress.services import get_user_statuses

from erajp.converter import strjpftime


def count_pj(steps, step_counter=0):
    num_pj = len(Counter([step.project for step in steps]))
    return num_pj


def round_big_int_to_99(num):
    if num > 99:
        return '99+'
    else:
        return num


class Panel:
    def __init__(self, course_steps=None, group_length=None, course_length=None):
        if course_steps:
            self.grant_course = course_steps[0]
            self.steps = course_steps[1]
            self.empty = False
        else:
            self.empty = True
        self.group_length = group_length
        self.course_length = course_length

    @property
    def grant_group(self):
        with_term_grant_course = self.grant_course.with_term_grant_courses.first()
        return with_term_grant_course.with_term_grant_group.grant_group

    @property
    def overdue_statuses_link(self):
        progress_index_link = reverse_lazy('progress:index')
        get_params = '?'
        today = date.today()
        get_params += 'date_to={t}'.format(t=today)
        get_params += '&grant_course={c}'.format(c=self.grant_course.id)
        return progress_index_link+get_params

    @property
    def num_step(self):
        # counter = 0
        # for s in self.steps:
        #     if s.due_date <= date.today():
        #         counter += 1
        return len(self.steps)

    # これを呼び出す
    @property
    def num_step_display(self):
        return round_big_int_to_99(self.num_step)

    @property
    def num_pj(self):
        return count_pj(self.steps)

    @property
    def num_pj_display(self):
        return round_big_int_to_99(self.num_pj)

    @property
    def class_(self):
        if self.empty:
            return 'info'
        if self.num_todo_today:
            return 'danger'
        else:
            return 'info'

    @property
    def is_margin(self):
        if self.num_todo_today:
            return ''
        else:
            return 'margin'


def today_overdue_status_str(user):
    today = date.today()
    today_status = get_user_statuses(user).filter(
        status_due_date__due_date__lt=today)

    client_staff_num = today_status.count()

    client_list = []
    for s in today_status:
        client = s.project.client_staff.client
        if client not in client_list:
            client_list.append(client)
    client_num = len(client_list)

    today_in_jp_str = strjpftime(datetime.combine(today, time()), '%O%E年%m月%d日')

    today_overdue_status_str = '本日（{t}）の締め切り　{c}社　{s}名'.format(
        t=today_in_jp_str, c=client_num, s=client_staff_num)

    return today_overdue_status_str
