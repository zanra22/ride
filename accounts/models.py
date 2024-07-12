from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


#User manager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        user_obj = self.model(email=self.normalize_email(email), **extra_fields)
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password, **extra_fields):
        extra_fields.setdefault('staff', True)
        extra_fields.setdefault('admin', False)
        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('staff', True)
        extra_fields.setdefault('admin', True)
        extra_fields.setdefault('active', True)
        extra_fields.setdefault('role', 'Admin')

        if extra_fields.get('staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        return self.create_user(email, password, **extra_fields)



#User models
class User(AbstractBaseUser):
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=50) #User`s role (Admin, Moderator, User)
    first_name = models.CharField(max_length=50, blank=True, null=True) #User`s first name
    last_name = models.CharField(max_length=50, blank=True, null=True) #User`s last name
    email = models.EmailField(max_length=50, unique=True) #User`s email
    phone_number = models.CharField(max_length=50, blank=True, null=True) #User`s phone number
    active = models.BooleanField(default=True) #User`s active status (Active, Inactive)
    staff = models.BooleanField(default=False) #User is a staff member
    admin = models.BooleanField(default=False) #User can log into the Django Admin
    created_at = models.DateTimeField(auto_now_add=True) #User`s creation date
    updated_at = models.DateTimeField(auto_now=True) #User`s last update date

    USERNAME_FIELD = 'email' #User`s email will act as the login credential
    REQUIRED_FIELDS = [] #Fields that will be required when running command `python manage.py createsuperuser`


    objects = UserManager()


    def __str__(self):
        return self.email #User`s email will be displayed in the Django Admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active




