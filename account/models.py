from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Custom User Models

class MyAccountManager(BaseUserManager):

    #create normal user
    def create_user(self, email, first_name, last_name, username, password=None):
        if not email:
            raise ValueError('Email not found')
        
        if not username:
            raise ValueError('Username not foound')
        
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # creating super uer
    def create_superuser(self, email, first_name, last_name, username, password):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name = last_name,
            username = username,
            password = password
        )

        user.is_admin = True
        user.is_superadmin = True
        user.is_staff = True
        user.is_active = True

        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superadmin

    def has_module_perms(self, app_label):
        return True