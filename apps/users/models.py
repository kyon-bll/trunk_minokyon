from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator

from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """カスタムユーザーモデル."""

    username_validator = ASCIIUsernameValidator()  # デフォルトでは Unicode でバリデートする

    # validator を override
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    geek_point = models.IntegerField('ギークポイント', default=0)

    @property
    def geek_rank(self):
        if self.geek_point == 0:
            return 0
        elif self.geek_point < 100:
            return 1
        elif self.geek_point < 77777:
            return 2
        elif self.geek_point < 530000:
            return 3
        else:
            return 4

    @property
    def full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    class Meta(AbstractUser.Meta):
        db_table = 'u_auth_user'
