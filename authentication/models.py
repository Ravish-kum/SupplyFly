from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
# Create your models here.

class UserManger(BaseUserManager):
    def __create(self,phone_number, company, city, address, password, is_staff, is_superuser, **extrafields):
        if not phone_number:
            return ValueError('phone number is not provided')
        user = self.model(phone_number = phone_number,address = address, city = city, company= company,
                          is_staff = is_staff, is_superuser = is_superuser, **extrafields )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,phone_number, company, city, address, password, **extrafields):
        return self.__create(phone_number = phone_number,address = address, city = city, password= password,
                            company= company, is_staff = True, is_superuser = True, **extrafields )
    
    def create_user(self,phone_number, company, city, address, password, **extrafields):
        return self.__create(phone_number = phone_number,address = address, city = city, password= password,
                             company= company, is_staff = False, is_superuser = False, **extrafields )


class User(AbstractUser,PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique = True)
    company_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username','company_name', 'city']
    class Meta:
        db_table = 'User'

