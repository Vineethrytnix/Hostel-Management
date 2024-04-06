from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Login(AbstractUser):
    userType = models.CharField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)
    
class UserReg(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=300, null=True)
    image = models.ImageField(null=True, upload_to="profile")
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)  
    
class Hosteller_reg(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=300, null=True)
    image = models.ImageField(null=True, upload_to="profile")
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True) 
    

class Blocks(models.Model):
    name = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='block_images/')
    block_no = models.CharField(max_length=300, blank=True)
    no_of_rooms = models.IntegerField(default=0)
    description = models.CharField(max_length=300, null=True)
    
class Rooms(models.Model):
    name = models.CharField(max_length=100, null=True)
    block=models.ForeignKey(Blocks, blank=True,on_delete=models.CASCADE,default=0)
    price = models.IntegerField(null=True, blank=True)
    room_no = models.CharField(max_length=300, blank=True)
    no_of_adults = models.CharField(max_length=300, blank=True)
    size = models.CharField(max_length=300, blank=True)
    image = models.FileField(upload_to='room_images/',default="image")
    image2 = models.FileField(upload_to='room_images/',default="image1")
    image3 = models.FileField(upload_to='room_images/',default="image2")
    description = models.CharField(max_length=300, null=True)
    type = models.CharField(max_length=300, null=True)

    
class Events(models.Model):
    name = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    image = models.FileField(upload_to='event_images/',default="event_image")
    end_time = models.TimeField(null=True)
    description = models.CharField(max_length=300, null=True)
    

class Mess_food(models.Model):
    day=models.CharField(max_length=100,null=True)
    breakfast=models.CharField(max_length=100,null=True)
    lunch=models.CharField(max_length=100,null=True)
    dinner=models.CharField(max_length=100,null=True)
    
    
class Room_booking(models.Model):
    check_in=models.DateField(null=True)
    check_out=models.DateField(null=True)
    adults=models.IntegerField(null=True, blank=True)
    amount=models.IntegerField(null=True, blank=True)
    date=models.DateField(auto_now_add=True, null=True, blank=True)
    status=models.CharField(max_length=100,null=True,default="Booked")
    pay_status=models.CharField(max_length=100,null=True,default="null")
    uid=models.ForeignKey(UserReg, on_delete=models.CASCADE, null=True, blank=True)
    gid=models.ForeignKey(Hosteller_reg, on_delete=models.CASCADE, null=True, blank=True)
    rid=models.ForeignKey(Rooms,on_delete=models.CASCADE, null=True, blank=True)
    type=models.CharField(max_length=100,null=True)
    
    
class Hosteller(models.Model):
    uid=models.ForeignKey(UserReg, on_delete=models.CASCADE, null=True, blank=True)
    bid=models.ForeignKey(Room_booking,on_delete=models.CASCADE, null=True, blank=True)
    status=models.CharField(max_length=100,null=True,default="Hosteller")
    
    
class Attendance(models.Model):
    uid=models.ForeignKey(UserReg, on_delete=models.CASCADE, null=True, blank=True)
    date=models.DateField(null=True)
    status=models.CharField(max_length=100,null=True,blank=True)
    
class Fees_structure(models.Model):
    desc=models.CharField(max_length=100,null=True)
    price=models.IntegerField(null=True, blank=True)
    date=models.DateField(auto_now_add=True,null=True, blank=True)
    
class Feedback(models.Model):
    rating=models.IntegerField(null=True, blank=True)
    comment=models.CharField(max_length=100,null=True)
    uid=models.ForeignKey(UserReg, on_delete=models.CASCADE, null=True, blank=True)
    gid=models.ForeignKey(Hosteller_reg, on_delete=models.CASCADE, null=True, blank=True)
    type=models.CharField(max_length=100,null=True,blank=True)
    
class Leave(models.Model):
    uid=models.ForeignKey(UserReg, on_delete=models.CASCADE, null=True, blank=True)
    date=models.DateField(null=True,auto_now_add=True)
    fromdate=models.DateField(null=True)
    todate=models.DateField(null=True)
    no_of_days=models.IntegerField(null=True, blank=True)
    status=models.CharField(max_length=100,null=True,blank=True,default="Requested")
    reason=models.CharField(max_length=100,null=True,blank=True)