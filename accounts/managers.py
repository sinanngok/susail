from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
import datetime


class UserManager(BaseUserManager):
    def _create_user(self, su_id, first_name, last_name, email, phone_number, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email and not su_id: #to contact SU students at least student id or email address is required
            raise ValueError('Users must have an email address or SU ID')
        email = self.normalize_email(email)

        user = self.model(
            su_id=su_id,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=self.normalize_email(email),
            password=BaseUserManager.make_random_password(self, length=8),
            ** extra_fields
        )

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, su_id, first_name, last_name, email, phone_number, password=None, **extra_fields):
        """
        Creates and saves a User with the given su_id, first_name, last_name, email, phone_number and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        self.password = BaseUserManager.make_random_password(self, length=8)

        return self._create_user(su_id, first_name, last_name, email, phone_number, password, **extra_fields)

    def create_superuser(self, su_id, first_name, last_name, email, phone_number, password , **extra_fields):
        """
        Creates and saves a superuser with the given su_id, first_name, last_name, email, phone_number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(su_id, first_name, last_name, email, phone_number, password, **extra_fields)