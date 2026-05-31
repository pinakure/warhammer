from django.views.decorators.csrf   import csrf_exempt
from django.template.loader         import render_to_string
from django.contrib.auth            import login, authenticate, logout
from django.shortcuts               import render, redirect 
from django.http                    import HttpResponse, JsonResponse
from django.conf                    import settings
from collections                    import namedtuple
from .models                        import *
    
__Unit = namedtuple('__Unit', ['value', 'name'])

def get_lexic(lang='en'):    
    if   lang=='en': from .lex_en import lex
    elif lang=='es': from .lex_es import lex
    return lex

def get_logo(game_id):
    game = Game.objects.get(id=game_id)
    return game.picture.url if game.picture else ''

def get_page(lang='es', game=1, army=-1):
    return {
        'language'  : lang,
        'game'      : game,
        'root'	    : settings.URL_ROOT,
        'logo'      : get_logo(game),
        'army'      : army,
        'header'    : True,
        'units'     : [] if (army < 0) else [ __Unit(unit.pk, unit.title) for unit in Unit.objects.filter(army_id=army)],
        'armies'    : [ a.json() for a in Army.objects.filter(game=game)],
        'games'     : [ g.json() for g in Game.objects.all() ],
    }

def template_stats(request, context):       return render_to_string('datacard.html', context=context, request=request)
def template_stratagems(request, context):  return render_to_string('stratagems.html', context=context, request=request)
def template_main(request, context):        return render_to_string('warhammer.html', context=context, request=request)
def template_pictures(request, context):    return render_to_string('pictures.html', context=context, request=request)

@csrf_exempt
def view_get(request):
    unit_type = int(request.POST.get('type' , None))
    language  = request.GET.get('lang' , 'es')
    game      = int(request.GET.get('game' ,    1))
    army      = int(request.GET.get('army' ,   -1))
    if unit_type == None: 
        return JsonResponse({ 'errorResponse' : f'Unknown unit type: {unit_type}'}, status=406)
    context  = { 
        'stratagems': [] if (army < 0) else [ q.json(army) for q in Army.objects.filter(id=army).get().stratagems.all() ],
        'unit'      : Unit.objects.filter(id=unit_type).get().json(), 
        'page'      : get_page(language, game, army), 
        'lex'       : get_lexic(language), 
    }
    return JsonResponse({ 
        'data'      : template_stats(request, context),
        'pictures'  : template_pictures(request, context),
        'stratagems': template_stratagems(request, context),
    }, status=200)

def view_login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    next = request.POST.get('next', request.GET.get('next', settings.URL_ROOT))
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(next)
    return render(request, 'login.html', context={ 'next' : next, 'root' : settings.URL_ROOT, 'username' : username, 'password' : password }) 

def view_logout(request):
    logout(request)
    return redirect(settings.URL_ROOT)

def view_main(request):    
    language = request.GET.get('lang', 'es')    
    game     = int(request.GET.get('game',    1))
    army     = int(request.GET.get('army',   -1))
    return render(request, 'warhammer.html', context={ 
        'page' : get_page(language, game, army),
        'lex'  : get_lexic(language), 
    })
    