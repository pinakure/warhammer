from django import template
from datetime import datetime, timedelta
from django.core.files.storage import default_storage
from django.contrib.auth.models import Group
from django.shortcuts import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.utils.html import mark_safe


register = template.Library()

@register.filter(name='initials')
def initials(data):
    parts = data.split(' ')
    ret = data[0]
    for p in parts[1:]:
        ret = ret + p[0]
    return ret

@register.filter(name='evaluate')
def evaluate(data):
    return eval(data)

@register.filter(name='plusone')
def plusone(data):
    return int(data)+1

@register.filter(name='leftright')
def leftright(data):
    i = int(data)
    if i % 2 == 0: return 'left'
    return 'right'

@register.filter(name='keyword_row')
def keyword_row(data):
    for d in data:
        name = data[d]['name']
        kset = data[d]['keywords']
        if len(kset)==0 :continue
        kwords = f' ({name})' if name else ''
        keyset = str(kset).replace('[', '').replace(']','').replace("'", "")
        return mark_safe(f'<tr><td>KEYWORDS{kwords}</td><td>{ keyset }</td><td ></td></tr>')
    return ""
    
@register.filter(name='color_cycle')
def color_cycle(data):
    ret = ""
    for a in data:
        ret = f'{ret}<cc>{a}</cc>'
    return ret

@register.filter(name='each_three')
def each_three(number):
    if number % 3 == 1: return True
    return False