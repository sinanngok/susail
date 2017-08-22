from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
import datetime

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given username, email and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    susail_id = models.AutoField(primary_key=True)
    username = models.CharField(('username'), max_length=30, blank=True, null=False, unique=True, )
    first_name = models.CharField(('first name'), max_length=30, blank=True, null=False)
    last_name = models.CharField(('last name'), max_length=30, blank=True, null=False)
    su_id = models.IntegerField(blank=True, null=False, unique=True, )
    email = models.EmailField(verbose_name='email address', max_length=255, )

    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number = models.CharField(validators=[phone_regex], blank=True)  # validators should be a list

    # django-phonenumber-field 1.1.0 ??
    # https://pypi.python.org/pypi/django-phonenumber-field/1.1.0

    phone_number = models.CharField(max_length=15, blank=True, null=False)
    emergency_contact_name = models.CharField(('first name'), max_length=30, blank=True, null=False)
    emergency_phone_number = models.CharField(max_length=15, blank=True, null=False)

    date_of_birth = models.DateField(('doğum tarihi'), blank=True, null=True)
    dept = model.IntegerField(('borç'), blank=True, null=True, )

    #custom sailing_levelField?
    sailing_level = model.IntegerField(('yelken seviyesi'), blank=True, null=True, )

    yonetim_kurulu_gorevi = models.CharField(('yönetim kurulu görevi'), max_length=30, blank=True, null=False,)
    yaris_takimi_pozisyonu = models.CharField(('yarış takımı pozisyonu'), max_length=30, blank=True, null=False,)

    extra_information = models.TextField(blank=True, null=False,)

    disweb = models.BooleanField()


    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)

    last_visit = models.DateTimeField(default=timezone.now, blank=True, null=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def was_active_recently(self):
        now = timezone.now()
        return self.last_visit >= timezone.now() - datetime.timedelta(minutes=15)
        was_active_recently.boolean = True

    def get_full_name(self):
        # Returns the first_name plus the last_name, with a space in between.
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        # Returns the short name for the user.
        return self.first_name

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin