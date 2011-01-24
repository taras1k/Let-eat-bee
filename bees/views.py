# Create your views here.
import urllib
from django.conf import settings
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from mongoengine import *
from models import *
from django.views.decorators.csrf import csrf_exempt
from forms import *
from django.template import Context, RequestContext 

def need_login(function):
    def wrap(request, *args, **kwargs):
        if 'user_id' not in request.session.keys():
            return redirect('/bees/login')
        return function(request, *args, **kwargs)
        wrap.__doc__=function.__doc__
        wrap.__name__=function.__name__
    return wrap


@csrf_exempt
@need_login
def homepage(request):
#    if 'user_id' in request.session:
#        user_loged = get_user(request.session['user_id'])
#        if user_loged.is_authenticated():
#            request.session['user_id'] = user_loged.id
#    else:
#        return redirect('/bees/login')    
    user_loged = get_user(request.session['user_id'])
    if request.method == 'POST':
        if request.POST['bee']  != '':
           event_n = request.POST['bee'] 
           #user_db, created = Users.objects.get_or_create(user_name =user_n)
           bees_event = Events(title = event_n, creator = user_loged)
           bees_event.save()
    bees = Events.objects
    title = 'Home, sweat home'
    return render_to_response("bees/home.html", locals(), context_instance=RequestContext(request))

def _register_user(user_data):
    User.create_user(user_data['username'], user_data['password'], user_data['email'])
    #user = User(username = user_data['username'], user_password = user_data['password'], user_mail = user_data['mail'], user_first_name = user_data['first_name'], user_last_name = user_data['last_name'])
    #user.save()



    

@csrf_exempt
def login(request):
    if 'user_id' in request.session:
        user_loged = get_user(request.session['user_id'])
        if user_loged.is_authenticated():
            request.session['user_id'] = user_loged.id
            return redirect('/bees')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_loged = _authenticate(form.data['user_name'], form.data['user_password'])
            if user_loged is not None:
                user_loged = User.objects.get(username = form.data['user_name'])
                request.session['user_id'] = user_loged.id
                return redirect('/bees')
    else:
        form = LoginForm()
    return render_to_response('bees/login_page.html', {
        'form': form,
    }, context_instance=RequestContext(request))


@csrf_exempt
def register(request):
    if 'user_id' in request.session:
        user_loged = get_user(request.session['user_id'])
        if user_loged.is_authenticated():
            request.session['user_id'] = user_loged.id
            return redirect('/bees')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_data = {'username':form.data['user_name'], 'password':form.data['user_password'], 'email':form.data['user_mail'], 'first_name':form.data['user_first_name'], 'last_name':form.data['user_last_name']}
            _register_user(user_data)
            return redirect('/bees')
    else:
        form = RegisterForm()
    return render_to_response('bees/register_page.html', {
        'form': form,
    }, context_instance=RequestContext(request))

@csrf_exempt
def social_login(request):
    data = {}
    json = ''
    data['token'] = 'vgvfvf'
    if request.method == 'POST':
        data['token'] = request.POST['token']
    json_file = urllib.urlopen('http://loginza.ru/api/authinfo?token='+data['token'])
    for line in json_file:
        json += line             
    data['json'] = json    
    #return redirect('http://loginza.ru/api/authinfo?token='+data['token'])
    return render_to_response('bees/social_login.html',data, context_instance=RequestContext(request))#login_result


def _authenticate(username=None, password=None):
    user = User.objects(username=username).first()
    if user:
        if password and user.check_password(password):
            return user
    return None

def get_user(user_id):
    return User.objects.with_id(user_id)
