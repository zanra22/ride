from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

#User models

class User(AbstractBaseUser):
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=50) #User`s role (Admin, Moderator, User)
    first_name = models.CharField(max_length=50) #User`s first name
    last_name = models.CharField(max_length=50) #User`s last name
    email = models.CharField(max_length=50) #User`s email
    phone_number = models.CharField(max_length=50) #User`s phone number
    active = models.BooleanField(default=True) #User`s active status (Active, Inactive)
    staff = models.BooleanField(default=False) #User is a staff member
    admin = models.BooleanField(default=False) #User can log into the Django Admin
    created_at = models.DateTimeField(auto_now_add=True) #User`s creation date
    updated_at = models.DateTimeField(auto_now=True) #User`s last update date

    USERNAME_FIELD = 'email' #User`s email will act as the login credential
    REQUIRED_FIELDS = [] #Fields that will be required when running command `python manage.py createsuperuser`

    def __str__(self):
        return self.email #User`s email will be displayed in the Django Admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_staff

    @property
    def is_admin(self):
        return self.is_admin

    @property
    def is_active(self):
        return self.is_active




