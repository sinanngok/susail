from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
import datetime

from .models import User

class UserManager(BaseUserManager):
    def create_user(self, su_id, first_name, last_name, email, phone_number, password=None):
        """
        Creates and saves a User with the given su_id, first_name, last_name, email, phone_number and password.
        """
        if not email and not su_id: #to contact SU students at least student id or email address is required
            raise ValueError('Users must have an email address or SU ID')

        user = self.model(
            su_id=su_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            email=self.normalize_email(email),
            password=make_random_password(length=8)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, su_id, first_name, last_name, email, phone_number, password):
        """
        Creates and saves a superuser with the given su_id, first_name, last_name, email, phone_number and password.
        """
        user = self.create_user(
            su_id,
            first_name,
            last_name,
            email,
            phone_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user