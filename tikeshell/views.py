from django.shortcuts import render
from tikeshell.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import  HttpResponse,JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login
from pprint import pprint as pp
from itertools import chain
import time,json,string,random
from io import StringIO
from tikeshell.utils import qrcodeGenerator
from django.contrib import messages
import smtplib
from tikeshell.utils import directpaylib as dpapi
from smsapi.client import SmsAPI
from smsapi.responses import ApiError
from django.shortcuts import get_object_or_404
#Global values
views='/'
global authentic#remove use django auth
authentic="0"

#utility functions
class ticket_view(object):
    '''
    used encode a ticket data to be used in the profile template 
    '''
    def __init__(self):
        self.id=None
        self.title=None
        self.venue=None
        self.date=None
        self.pin=None
        self.image_url=None

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    generate a 6 character pi that is unique in db/ticket
    """
    pin=''.join(random.choice(chars) for _ in range(size))
    if Ticket.objects.filter(pin=pin).count() !=0:
        id_generator()
    else:
        return pin

def longdiv(divisor,divident): #hha longdiv is a better name i geuss
  quotient,remainder=divmod(divisor,divident)
  return quotient,remainder

def sort(_list):
    _list.sort()
    return(_list)

def highest_vals_calc(vals,lookup=3):
    vals.sort(reverse=True)
    return vals[:lookup]

def save_to_string(img):
    obj=StringIO()
    img.save(obj,format='PNG',quality=90)
    obj.seek(0)
    return obj.read()

def get_cols(data,cols=2):
    if len(data)<cols:
        for i in range(cols-len(data)):
            data.append(None)
    elif len(data)<cols*2:
        for i in range((cols*2)-len(data)):
            data.append(None)
    pts,rem=longdiv(len(data),cols)
    chunks=[]
    chunk=[]
    cnt=1

    for d in data:
        chunk.append(d)
        if cnt==pts:
            chunks.append(chunk)
            cnt=0
            chunk=[]
        cnt+=1

    cnt=0
    for d in data[pts*cols:]:
        chunks[cnt].append(d)
        cnt+=1
    return chunks

def get_similar_events(event,choices=3):
    '''
    get event that have at least one tag in common
    choose 3{?} of which have the most common tags
    i have used iterators as oftenly possible as i can 
    to reduce the time it takes per loop but still it loops alot
    i have introduced a timer that will stop the main big loop after 0.5 sec max
    so it won't ever cause serious trouble, use less memmory too than before
    '''
    tags=event.tags
    same_tag={}
    begin_time=time.time()
    for tag in tags.iterator():
        if time.time()-begin_time>0.5: #no matter what size spend only 0.5 sec here, dumb i know :(
            break
        #maybe by using select_related[?] we can go still faster[?]
        for event_ in tag.show_set.all().exclude(id=event.id):
            same_tag.setdefault(event_.id,0)
            same_tag[event_.id]+=1

    query=Q()
    highest_vals=highest_vals_calc(same_tag.values(),choices)
    for key,val in same_tag.iteritems(): #use iterator cause it's faster that items list
        if val in highest_vals:
            query |= Q(id=key)

    return Show.objects.filter(query)
#security vurnelability here ,if you where to generate random pins and requests their qrcodes...
#{don't consider} this is part of our api, so we request an api_token, plus we get someone to blame on error :)
#will look into a more serious security for this func
#this ain't a fix at all because if we put a token everyone can see ours when we call it
#for lack of a better security idea i will pass all of the text to this func,no way can they hack this
#anyway feel free to improve on this, and don;t make something that write qrcode on the filesys
#this func was made entirely so we generate qrcodes without the need of any temp filesys
#last try is to make this as an object of the Ticket models class and call it on the ticket simply
#this will not show any vurnelabilities
#tried it but we can't output directly a return HttpResponse in html
def render_qrcode(request,text): #this is considered a helper function not really a view func
    '''
    #this here is just for the idea of the previous and projected work that had security vurnelabilities
    if not api_token: #verify the token
        return HttpResponse('<h2>Not Allowed</h2>',content_type='text/html') #replace with a 404
    try:
        ticket=Ticket.objects.get(pin=ticket_pin)
    except:
        return HttpResponse('<h2>None</h2>',content_type='text/html') #replace with a 404
    event_name=Show.objects.get(id=ticket.event_id)
    text='name: %s event: %s pin: %s' % (ticket.full_name,event_name,ticket.pin)'''
    qrcode=save_to_string(qrcodeGenerator.init(text)) #render and save it in mem
    response= HttpResponse(qrcode,content_type='image/png') 
    return response
#next is the function that renders the hallmap
#def render_hallmap(event):
 #   color_keys={}
  # None
# Create your views here vyhvkfghvmvm
def home(request):
    global views
    global authentic
    views='/'
    all_events={}
    primary_event= Show.objects.get(level__level="Main")
    all_events= Show.objects.filter(level__level="Important")
    if request.user.is_authenticated:
        user=request.user
        account=Account.objects.get(user=user)
    for event in all_events:
        if event.level.level == "Main":
            primary_event=event

    n_el= len(all_events)
    shows=0
    if n_el<=2:
        #shows=0
        events_all=all_events

    else:
        events_all=all_events
        '''list_event_child=0
        while n_el > 2:
            shows={}
            list_event_child={}
            list_event_child.append(all_events[0:3])
            shows.append(list_event_child)
            all_events[0:1].remove()
            if n_el1 <= 2:
                list_event_child.append(all_events)
                all_events.clear()'''
        

    all_other_events= Other_events.objects.all()
    n_el1=len(all_other_events)
    if n_el1 <= 2:
        other_events_all=all_other_events
        other_events=0
    else:
        other_events_all=all_other_events
        '''list_other_event_child=0
        list_other_event_child={}
        while n_el1 > 2:
            other_events={}
            other_event_child.append(all_other_events[0:3])
            other_events.append(list_other_event_child)
            all_other_events[0:3].remove()
            
            n_el1= len(all_other_events)
            if n_el1 <= 2:
                list_other_event_child={}
                list_other_event_child.append(all_other_events)'''
    events=list(chain(all_events, all_other_events))
    '''
    nkeys= int(len(events)/2)
    print(nkeys)
    remainder= len(events) % 2
    col1=list()
    col2=list()
    if remainder==0:
        col1.extend(events[0:nkeys])
        col2.extend(events[nkeys+1:len(events)])

    elif remainder==1:
        nkeys +=1
        col1.extend(events[0:nkeys])
        col2.extend(events[nkeys:len(events)]) 
    '''
    col1,col2=get_cols(events)
    '''
    if authentic == "0":
        name=0

    else:
        name=authentic.full_name
    '''
    return render(request,'html/index.html',locals())
def event(request,id):
    global views 
    views='event'
    return render(request,'html/event.html',{})
def all(request):
    #get events in that category
    #order by likes or such thin
    if request.user.is_authenticated:
        user=request.user
        account=Account.objects.get(user=user)
    global views
    global authentic
    views="/all/"
    all_events={}
    all_events= list(Show.objects.all())  
    all_other_events= list(Other_events.objects.all())
    print (len(all_events))
    print (get_cols(all_events,3))
    ecols=get_cols(all_events,3)
    ocols=get_cols(all_other_events,3)
    '''
    ekeys=int(len(all_events)/3)
    eremainder=len(all_events) % 3
    okeys=int(len(all_other_events)/3)
    oremainder=len(all_other_events) % 3
    ecol1=list();ecol2=list();ecol3=list()
    ocol1=list();ocol2=list();ocol3=list()
    if eremainder==0:
        ecol1.extend(all_events[0:ekeys])
        ecol2.extend(all_events[ekeys:ekeys*2])
        ecol3.extend(all_events[ekeys*2: len(all_events)])


    elif eremainder==1:
        init=ekeys+1
        ecol1.extend(all_events[0:init])
        ecol2.extend(all_events[init:ekeys*2])
        ecol3.extend(all_events[ekeys*2: len(all_events)])

    elif eremainder==2:
        init=ekeys+1
        ecol1.extend(all_events[0:init])
        ecol2.extend(all_events[init:ekeys*2+2])
        ecol3.extend(all_events[ekeys*2+2: len(all_events)])
    
    if oremainder==0:
        ocol1.extend(all_other_events[0:okeys])
        ocol2.extend(all_other_events[okeys:okeys*2])
        ocol3.extend(all_other_events[okeys*2: len(all_events)])


    elif oremainder==1:
        init=okeys+1
        ocol1.extend(all_other_events[0:init])
        ocol2.extend(all_other_events[init:okeys*2])
        ocol3.extend(all_other_events[okeys*2: len(all_events)])

    elif oremainder==2:
        init=okeys+1
        ocol1.extend(all_other_events[0:init])
        ocol2.extend(all_other_events[init:okeys*2+2])
        ocol3.extend(all_other_events[okeys*2+2: len(all_events)])

    ecols=list(); ocols=list()
    ecols.append(ecol1);ecols.append(ecol2);ecols.append(ecol3)
    ocols.append(ocol1);ocols.append(ocol2);ocols.append(ocol3)
    '''
    '''
    if authentic == "0":name=0

    else:
        name=authentic.full_name
    '''
    return render(request,'html/all.html',locals())



def loginpg(request):
    global views
    global authentic
    #current login  should use django oAuth
    if request.method=='POST':
        email= request.POST['email']
        password=request.POST['password']
        authentic=0
        try:
            user=authenticate(username=email,password=password)
            authentic=Account.objects.get(user=user)# Do not complicate stuff
            '''if user:
                login(request,user)
                authentic= Account.objects.get(user=user)
                if 'next' in request.GET.keys():#why doesn't it work?
                    return HttpResponseRedirect(request.GET['next'])'''
            if views=="/":
                return HttpResponseRedirect('/')
            else:  
                url=views
                return HttpResponseRedirect(url)
        except Account.DoesNotExist:
            messages="Wrong email and password combination"
            return render(request,'html/login.html', locals())
            
    else:
        if views == "/signup/":
            views="/"
            return render(request,'html/login.html',{'messageSignUp':'You have successful signed in!'})
        else:
            return render(request,'html/login.html',{})

def search(request):
    if request.user.is_authenticated:
        user=request.user
        account=Account.objects.get(user=user)
    if request.method=='GET':
        try:
            q=request.GET['q']
            event_query=Q(Q(title__contains=q)|Q(description__contains=q))
            other_event_query=Q(Q(title__contains=q)|Q(description__contains=q))
            for word in q.split(' '):
                event_query |= Q(Q(title__contains=word)|Q(description__contains=word))
            event_results=Show.objects.filter(event_query)#maybe put tags and reviews too
            other_events_results=Other_events.objects.filter(event_query)
    #mix queuries and sort them 
            print (q,'\n',event_results,'\n')
            cols=get_cols(list(chain(list(event_results),list(other_events_results))))
            print(cols)
            if cols[0] == [None]:
                cols=0
                print(cols)
            return render(request,'html/search.html',locals())
        except KeyError:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def signup(request):
    global views
    views="/signup/"
    if request.method=='POST':
        try:
            email= request.POST['email']
            name=request.POST['name']
            password= request.POST['password']
            phone= request.POST['phone']
            status=Account.objects.filter(email=email)
            if len(status)>0:
                return render(request,'html/signup.html',{'message':'You did not successful sign up. Please use another email.'})
            else:
                user = User.objects.create_user(username=email,password=password)
                profile= Account(email=email, full_name=name,user= user, phone_number=phone)
                profile.save()
                return HttpResponseRedirect('/login/')

        except KeyError:
            return render(request,'html/signup.html',{'message':'You did not successful sign up. Please use another email.'})
    else:
        return render(request,'html/signup.html',{})
@login_required
def entertainment(request,event_id):
    #TODO:autofill payment fields[done]
    previous_url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        user=request.user
        account=Account.objects.get(user=user)
        event=get_object_or_404(Show,id=event_id)
    if 'message' in request.POST.keys():
        rating=int(request.POST['rating'])
        if rating >10: rating=10
        new_comment=comment.objects.create(text=request.POST['message'],event=event,user=account,date=datetime.datetime.now(),rating=rating)
        new_comment.save()    
    comments=comment.objects.filter(event=event).order_by('-date')
    tickettypes= tickettype.objects.filter(event=event_id)
    return render(request,'html/cart.html',locals())
@login_required
def educational(request, event_id):
    if request.user.is_authenticated:
        user=request.user
        account=Account.objects.get(user=user)
    event=get_object_or_404(Other_events,id=event_id)
    badgetypes= badgetype.objects.filter(event=event_id)
    return render(request,'html/cart_other.html', locals())
#@login_required 

def support(request):
    #an html page explaining the process of buying a ticket & which may also include a way to ask for help
    if request.user.is_authenticated:
        user=request.user
        account=Account.objects.get(user=user)
    if request.method=='POST':
        try:
            email= request.POST['email']
            name=request.POST['name']
            message=request.POST['message']
            if message is None:
                return render(request,'html/help.html')
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("tikerwanda@gmail.com", "kntberwa2017")
            msg = "Name:{{name}}/nEmail:{{email}}/n Message:{{message}}".format(name,email,message)
            server.sendmail("tikerwanda@gmail.com", "berwa05@gmail.com", msg)
            server.quit()
            return render(request,'html/help.html',{'message':'Your message was successful sent'},locals())

        except KeyError:
            return render(request,'html/help.html',{'message':'You did not submit your message./n Please try again'},locals())
    else:
        return render(request,'html/help.html',locals())

@login_required
def dashboard(request): # profile management
    #derive it from django.auth
    #basket=Ticket.objects.filter(user_id=user,payed=False)
    #my_tickets=Ticket.objects.filter(user_id=user,payed=True)
    #similar_events=get_similar_events(event,6) #PUBLICITY_EVENTS
    if request.user.is_authenticated:
        user=request.user
        account=Account.objects.get(user=user)
        abbr=''
        for word in account.full_name.split(' '):
            abbr+=word[0].upper()
        #add stuff for paying not payed tickets
        tickets=Ticket.objects.filter(user_id=user.id,payed=True)
        events=[]
        #find an efficient wway to do this
        for ticket in tickets:
            show=Show.objects.get(id=ticket.event_id)
            event=ticket_view()
            event.id=show.id
            event.title=show.title
            event.venue=show.venue
            event.image_url=show.image.url
            event.date=show.date
            event.pin=ticket.pin
            events.append(event)

        cols=get_cols(events)
        print(cols)
    return render(request,'html/profile.html',locals()) 
'''
def view_ticket(request,event_id):
    event=Show.objects.get(id=event_id)
    ticket_types=event.tickettypes.iterator()
    reviews=event.reviews.iterator()
    similar_events=get_similar_events(event,6)
    print (event.venue.name)
    #some hallmap processing here!
    #handle post events
    #when ticket specs selected and number 
    #create a new entry for all and mark them as not yet paid for
    return render(request,'html/view_ticket.html',locals())
    '''
'''
def ticket(request,ticket_pin):
    #ticket_pin='A1B2E3'
    ticket=Ticket.objects.get(pin=ticket_pin)
    event=Show.objects.get(id=ticket.event_id)
    tickets_avail=event.tickets_no-Ticket.objects.filter(event_id=event.id).count()
    tickets_sameName=Ticket.objects.filter(full_name=ticket.full_name).count()
    tickets_sameName_used=Ticket.objects.filter(full_name=ticket.full_name,used=True).count()
    qr_code_info='name: %s event: %s pin: %s' % (ticket.full_name,event.title,ticket.pin) #put some kind of encryption here
    return render(request,'html/ticket.html',locals())
    #great stark! We should work in this update function very soon!

    '''
def api_update_shows(request):#put a field of a password
    '''
    add info in db/shows, checks first if info is already in
    returns item.id if update and 0 if not
    '''
    '''
    TODO: make this functional
    i have skipped this because updating the db from onsite's data
    requires handling many uncertainities will work on this on v2
    '''
    fields={'id':'','title':'','category':'','desc':'','image':'','date':'','venue_info':'','num':'','tickettypes_info':'','organizer_info':''}
    for key in request.GET.keys():
        if key in fields.keys() and request.GET[key] not in ['']:
            fields[key]=request.GET[key]
    return JsonResponse({'info':'TODO'})
#def sitemap(request): NO need of a sitemap yet!
#	return render(request,'html/sitemap.html')

#def purchase(request):
@login_required
def pay_portal(request):
    previous_url = request.META.get('HTTP_REFERER')
    print(previous_url)

    if request.user.is_authenticated:
        account=Account.objects.get(user=request.user)
        if ['name','phone'] not in request.POST.keys():
            name=account.full_name
            phone=account.phone_number
            email=account.email
        else:
            name=request.POST['name']
            phone=request.POST['phone']
            email='tikerwanda@gmail.com'#put company email in settings
        try:
            if 'entertainment' in previous_url:
                event=Show.objects.get(id=int(request.POST['event_id']))
            elif 'educational' in previous_url:#oh no payment here hha over did again
                event=Other_events.objects.get(id=int(request.POST['event_id']))
            else:
                return HttpResponseRedirect(previous_url)
            amount=int(request.POST['amount'])
            if amount <=0:
                return HttpResponseRedirect(previous_url)
            tk_type=tickettype.objects.get(id=int(request.POST['type']))
            price=tk_type.amount*amount
            pin=id_generator()
            dpapi.dt['fname']=name
            dpapi.dt['lname']=' '.join(name.split(' ')[1:])
            dpapi.dt['email']=email
            dpapi.dt['phone']=phone
            dpapi.dt['price']=price
            if request.META['HTTP_HOST'] == None:
                return HttpResponseRedirect(previous_url)
            dpapi.dt['redirect-url']=request.META['HTTP_HOST']+'/validate?pin='+pin
            res=dpapi.create_token()
            newticket= Ticket.objects.create(event_id=event.id,
                pin=pin,full_name=name,tickettype_id=tk_type.id
                ,phone_number=phone,user_id=account.id,token=res['token'])
            newticket.save()
            print (res)
            print (request.META['HTTP_HOST']+'/validate?pin='+pin)
            print(res['url'])
            return HttpResponseRedirect(res['url'])
        except:
            return HttpResponseRedirect(previous_url)

def validate(request):
    try:
        pin=request.GET['pin']
        ticket=Ticket.objects.get(pin=pin)
        dpapi.ddt['transaction_token']=ticket.token
        event=Show.objects.get(id=ticket.event_id)
        tk_type=tickettype.objects.get(id=ticket.tickettype_id)
        dpapi.verify_token()
        ticket.payed=True
        ticket.save()
        #add sms stuff
        api = SmsAPI()
        api.set_username('tike')
        api.set_password('869579e0598bd70a216261a80507efed')
        api.auth_token = 'q6QWErR7qkI9MNzA4bJJ86fltC5KfselYYiO2DUi'
        api.service('sms').action('send')
        api.set_content('[%1%] this ticket is for [%2%] in [%3%] at [%4%] your pin is [%5%],Help Call: 07893637884 Thank you! TIKE.')
        api.set_params(ticket.full_name,event.title,tk_type.tike_type,event.date.strftime("%d-%b at %H:%M"),pin) 
        api.set_to(ticket.phone_number)
        api.set_from('Tike ltd') #Requested sender name
        result = api.execute()
        for r in result:
            print (r.id, r.points, r.status)
        return HttpResponseRedirect("/all")#render thank you page
    except:
        return HttpResponseRedirect("/")