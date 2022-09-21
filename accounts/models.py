from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class UserManager(BaseUserManager):

    use_in_migrations = True


    def create_user(self, email, username, password):
        if not email:
            raise ValueError('must have user email')
        if not username:
            raise ValueError('must have username')
        if not password:
            raise ValueError('must have user password')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):

        user = self.create_user(
           email=self.normalize_email(email),
           username=username,
           password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    objects = UserManager

    username = models.CharField(_('username'), max_length=50, validators=[username_validator], blank=True)
    email = models.EmailField(_('email_adress'), unique=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date join'), auto_now_add=True)

    object = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    PASSWORD_FIELD = 'password'
    REQUIRED_FIELDS = ['username', 'password']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def is_staff(self):
        return self.is_superuser

    def email_user(self, subject, message, from_email = None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)