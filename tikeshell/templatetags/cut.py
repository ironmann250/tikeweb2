from django import template                                                                                                              
from django.conf import settings                                                                                                     

register = template.Library()                                                                                                      
@register.filter(name='cut')                                                                                                  
def cut(value,old='/'):                                                                                                                                                                                                                       
    return value.replace(old,'')
