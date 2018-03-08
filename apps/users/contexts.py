from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy


class MemberListContext:
    def __init__(self, request_user):
        self.user_group = request_user.groups.get()
        self.request_user_is_admin = bool(request_user.is_superuser)
        if request_user.has_perm('perm.is_sharoshi'):
            self.button_in_row = ['編集', '削除']
    column_names = ['ユーザー名', 'メールアドレス', '氏名', '権限', '登録日時', '']

    @property
    def row_lists(self):
        if self.request_user_is_admin:
            members = get_user_model().objects.all()
        else:
            members = get_user_model().objects.filter(groups=self.user_group)
        return [self.MemberRow(member) for member in members]

    class MemberRow:
        def __init__(self, member):
            self.member = member

        @property
        def items(self):
            items = [
                self.member.username,
                self.member.email,
                self.member.get_full_name,
                self.member.verbose_perm,
                self.member.date_joined,
            ]
            return items

        @property
        def buttons(self):
            button_dict_list = [
                dict(url=reverse_lazy('members:edit', args=[self.member.id]),
                     class_='btn-default'),
                dict(url=reverse_lazy('members:del', args=[self.member.id]),
                     class_='btn-danger')]
            return button_dict_list


class MemberAddModalContext:
    def __init__(self, form):
        self.form = form

    id = 'MemberAddModal'

    @property
    def button(self):
        return self.Button()

    class Button:
        class_ = 'btn-info'
        text = 'メンバー追加'

    @property
    def content(self):
        return self.Content(self.form)

    class Content:
        def __init__(self, form):
            self.form = form
        icon = 'user'
        text = '追加するメンバーの情報を入力してください。'
        title = 'メンバー追加'
        submit = '作成する'
