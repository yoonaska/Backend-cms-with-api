from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext as _
# Create your models here.


def users_image(self, filename):
    return f"users/{self.id}/{self.username}-{self.email}.png"

def users_default_image():
    return f"default/avatar/default-user-image.jpg"

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password = None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        if password:
            user.set_password(password)
            
        user.save()
        return user


    def create_superuser(self, email, password, phone, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('phone', phone)
    
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff = True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True.'))
        
        return self.create_user(email, password, **extra_fields)



class Users(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(_('Email'), max_length = 255, unique = True, blank = True, null = True)
    username = models.CharField(_('User Name'), max_length = 300, blank = True, null = True)
    first_name = models.CharField(_('First Name'), max_length = 200, blank = True, null = True)
    last_name = models.CharField(_('Last Name'), max_length = 200, blank = True, null = True)
    image = models.ImageField(_('Image'),upload_to=users_image, default=users_default_image)
    phone = models.CharField(_('Phone'), max_length = 20, unique= True, blank = True, null = True, help_text='Enter 10 digits phone number')
    date_joined = models.DateTimeField(_('Date Joined'),  auto_now_add = True, blank = True, null = True)
    last_login = models.DateTimeField(_('Last Login'),  auto_now = True, blank = True, null = True)
    otp = models.CharField(_('OTP'), max_length = 255, blank = True, null = True)
    
    is_verified           = models.BooleanField(default = False)
    is_admin              = models.BooleanField(default = False)
    is_active             = models.BooleanField(default = True)
    is_staff              = models.BooleanField(default = False)
    is_superuser          = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username','phone',]

    objects = UserManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj = None):
        "Does the user have a specific permission?"
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True


# class UserPermissions(Users):
#     class Meta:
#         proxy = True
#         permissions = [('Can customer user permissions', 'access_customerpermissions')]


