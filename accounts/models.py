from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
import datetime

from .managers import UserManager

class User(AbstractBaseUser):

    # susail_id in .mdb file might be directly pass to default id attribute
    #susail_id = models.AutoField(primary_key=True)
    first_name = models.CharField(verbose_name='first name', max_length=255, blank=True, null=False)
    last_name = models.CharField(verbose_name='last name', max_length=255, blank=True, null=False)
    su_id = models.IntegerField(blank=True, null=False, )
    email = models.EmailField(verbose_name='email address', max_length=255, )

    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number = models.CharField(validators=[phone_regex], blank=True)  # validators should be a list

    # django-phonenumber-field 1.1.0 ??
    # https://pypi.python.org/pypi/django-phonenumber-field/1.1.0

    # according to E.164 max. character length of a phone number is 15
    # localflavor libabry doesn't have PhoneNumberField for Turkey but TRIdentificationNumberField is valid for forms
    phone_number = models.CharField(max_length=15, blank=True, null=False)
    emergency_contact_name = models.CharField('first name', max_length=255, blank=True, null=False)
    emergency_phone_number = models.CharField(max_length=15, blank=True, null=False)
    date_of_birth = models.DateField(verbose_name='doğum tarihi', blank=True, null=True)
    is_entry_fee_paid = models.BooleanField(default=False)

    #custom sailing_levelField?
    sailing_level = models.IntegerField('yelken seviyesi', blank=True, null=True, )
    club_management_position = models.CharField(verbose_name='yönetim kurulu görevi', max_length=255, blank=True, null=False,)
    sailing_team_position = models.CharField(verbose_name='yarış takımı pozisyonu', max_length=255, blank=True, null=False,)
    extra_information_about_member = models.TextField(blank=True, null=False,)
    is_visible_on_web = models.BooleanField(default=True)
    date_joined = models.DateTimeField(verbose_name='kayıt tarihi', auto_now_add=True)
    is_an_active_student = models.BooleanField(default=True)
    is_school_staff = models.BooleanField(default=False)
    is_gorbon_captain = models.BooleanField(default=False)

    # is_eager_newbie_member?
    # newbie?
    # is_aktif_uye?
    # is_fresh_blood?
    is_active_member = models.BooleanField(default=False)

    # 'kredi' attribute will change to susail_balance
    # 'borç' attribute is not needed since balance can be both - & +
    susail_balance = models.IntegerField(blank=True, null=False,)

    last_visit = models.DateTimeField(default=timezone.now, blank=True, null=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['su_id']

    def was_active_recently(self):
        now = timezone.now()
        return self.last_visit >= timezone.now() - datetime.timedelta(minutes=15)

    def get_full_name(self):
        # Returns the first_name plus the last_name, with a space in between.
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        # Returns the short name for the user.
        return self.first_name

    def __str__(self):  # __unicode__ on Python 2
        return self.get_full_name

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