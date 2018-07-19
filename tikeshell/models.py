from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from io import StringIO
from django.contrib import admin
from random import randint
from django.utils import timezone
import datetime 
from tikeshell.utils import qrcodeGenerator
from django.http import HttpResponse
import random
today=datetime.datetime.today
random_number=int(random.random() * 1000)



# Create your models here.
class Keyword(models.Model):
    word=models.CharField(max_length=100)
    def __str__(self):
        return self.word

class Picture(models.Model): #add the thumb stuff::: done 
    image=models.ImageField(upload_to="event")#upload_to='photos' ? #thumbfield
    alt_text=models.TextField()
    def __str__(self):
        return self.alt_text

#no use now
'''
class MainPicture(models.Model):
    pass

    mainpicture= models.ManyToManyField(Picture)
    def __str__(self):
        return self.id
    '''
class Category(models.Model):
    category_title=models.CharField(max_length=100)#changed to this dumb name for the sake of a better representation in the admin filters
    description=models.TextField()
    class meta:
        plural='Categories' #not working why?
    def __str__(self):
        return self.category_title

class Account(models.Model):
    email=models.EmailField(blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=200)
    phone_number=models.BigIntegerField(blank=True)
    #address?
    #fav_tags=models.ManyToManyField(Category)
    
    def __str__(self):
        return self.full_name
class Admin:
    pass
class levels(models.Model):
    level=models.CharField(max_length=30)
    def __str__(self):
        return self.level
class Admin:
    pass

class Other_events(models.Model):
    title=models.CharField(max_length=100)
    description = models.TextField()
    Venue= models.CharField(max_length=100)
    date = models.DateTimeField(default=today())
    image=models.ImageField(upload_to="event")
    register_url= models.CharField(max_length=100, null=True)
    free=models.BooleanField(default=False)
    tags=models.ManyToManyField(Keyword)
    uniqint=models.IntegerField(default=random_number)
    level=models.ForeignKey(levels, on_delete=models.CASCADE)
    url=models.CharField(max_length=100, default="/educational/")
    if free:
        Price=0

    def __str__(self):
        return self.title
class Admin:
    pass



class Show(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    description = models.TextField()
    image=models.ImageField(upload_to="event")
    date = models.DateTimeField(default=today())
    venue= models.CharField(max_length=50)
    tickets_no = models.IntegerField( default=0)
    tags=models.ManyToManyField(Keyword)
    uniqint=models.IntegerField(default=random_number)
    level=models.ForeignKey(levels, on_delete=models.CASCADE)
    url=models.CharField(max_length=30, default="/entertainment/")#not needed we can know it trough other differences
    '''
    posters a variant of manytomany rel with pictures
    include or not?f
    '''
    def __str__(self):
        return self.title
class tickettype(models.Model):
    tike_type = models.CharField(max_length=100)
    amount = models.IntegerField()
    Content= models.CharField(max_length=100)
    event=models.ForeignKey(Show, on_delete = models.CASCADE)
    def __str__(self):
        return self.tike_type

class badgetype(models.Model):
    badge_type = models.CharField(max_length=100)
    amount = models.IntegerField()
    Content= models.CharField(max_length=100)
    event= models.ForeignKey(Other_events, on_delete = models.CASCADE)
class Admin:
    pass
#sellers
class SellerAccount(Account):
    hosted_shows=models.ManyToManyField(Show)
    introduction=models.TextField()
    #logo= models.ImageField(upload_to="logo")
    def __str__(self):
        return self.full_name
#again for a good usage of resources we don't save tickets with relations
#we have a dilemna should we use users or just plain entry forms?
#gonna use users for non users we wiil save with not_user set to true
#the above is just lack of time we could have set a new user and 
#deleted him after the transaction

#UPDate this to include the special tickets
#the straigghtforward way is to taake all free evvents as educationall
#above false ddrop other events annd makke it like sshow
class Ticket(models.Model):
    event_id=models.BigIntegerField() #because names overlap #thinking on making this a foreignKey
    pin=models.CharField(max_length=6)#upgrade at 6*(10**26)th ticket
    phone_number=models.BigIntegerField()
    email=models.EmailField(blank=True)
    full_name=models.CharField(max_length=200)
    tickettype_id=models.BigIntegerField()
    user_id=models.BigIntegerField()#user_id,"-1" when not a user
    payed=models.BooleanField(default=False)
    used=models.BooleanField(default=False)
    is_user=models.BooleanField(default=True)
    date=models.DateTimeField(default=today())
    token=models.CharField(max_length=72)
    def __str__(self):
        return self.full_name+": "+self.pin
    #this here produce the qrcode was wrote for security reasons
    #the issue is you can't output directly an httpresponse in a html doc
    #when solved there will be no vurnelabilities on the qrcode generation
    def _save_to_string(self,img):
        obj=StringIO()
        img.save(obj,format='PNG',quality=90)
        obj.seek(0)
        return obj.read()
    def render_qrcode(self):
        text='name: %s event_id: %s pin: %s' % (self.full_name,self.event_id,self.pin) #encrypt in some ways
        qrcode=self._save_to_string(qrcodeGenerator.init(text))
        return HttpResponse(qrcode,content_type='image/png')

class comment(models.Model):
    #idcomment= models.CharField(max_length= 10)
    text= models.CharField(max_length= 500)
    event= models.ForeignKey(Show, on_delete= models.CASCADE)
    user = models.ForeignKey(Account, on_delete= models.CASCADE)
    date = models.DateTimeField()
    rating= models.IntegerField()

    def __str__(self):
        return self.text[:20]+'...'

class stats(models.Model):
    None
    #put things as web_views,mem_usage[?],
#classes to represent models in the admin page
class AccountAdmin(admin.ModelAdmin):
    list_display = ('full_name','phone_number')
    search_fields = ('user__username','full_name','phone_number','email')

class ShowAdmin(admin.ModelAdmin):
    list_display = ('title','category','venue','date')
    search_fields = ('id','title','category','tags__word','venue__name','description')
    list_filter=('category__category_title','date')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('full_name','pin','phone_number','date')
    search_fields = ('full_name','pin','phone_number','email','event_id','tickettype_id')
    list_filter=('event_id','tickettype_id','used','is_user','date')

