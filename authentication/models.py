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
    company_name = models.ForeignKey('CompanyTable',verbose_name= "company_name",on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'city']
    class Meta:
        db_table = 'User'

class CompanyTable(models.Model):
    id = models.AutoField(primary_key= True)
    company_name = models.CharField(max_length = 50, unique = True)
    company_contact = models.CharField(max_length =13, blank = False, null = False)
    company_address = models.CharField(max_length =100, null = True, blank = True)
    user_count = models.IntegerField(default=0)
    class Meta:
        db_table = 'CompanyTable'