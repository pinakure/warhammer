from django.utils.html      import mark_safe
from random                 import random

def NaturalList(array):
    if len(array) == 1: return array[0]
    pre_last = len(array) -2
    ret = ''
    i = 0
    for e in array:
        last = i==pre_last+1
        ret += e 
        if i==pre_last: ret += ' y '
        elif not last: ret += ', ' 
        i+=1
    return ret

def PickAny(array):
    i = int(random()*len(array))
    return array[i]

class DescriptionRedactor:
    @staticmethod  
    def contains(crew):
        ret = f"Esta unidad { PickAny([ 'consta de', 'contiene']) } "
        last = len(crew)-2
        i=0
        for c in crew:
            ret += f"{c['quantity']} {c['name']}{'s' if c['quantity']>1 else ''}"+(" y" if i == last else " ,")
            i+=1
        return f'{ret[:-2]}'

    @staticmethod  
    def includes(crew):
        ret = ' Puede incluir '
        i=0
        last_item = len(crew)-2
            
        for c in crew:
            last = i == last_item
            plural = False if     c['quantity'] == 1 else True # since 0 is any number and > 1 is not singular...
            alt    = False if not c['alternative']   else True
            quantity = '' if not plural else ' hasta'
            sub = f"{ c['name'] }{'s' if plural else ''}"
            power = "" if ( c['power']==0 or alt ) else f"<b>(Potencia de unidad +{c['power']})</b>"
            if alt:
                ret = ret[:-2] + ' o '
            ret += f"{ quantity  } {c['quantity']} "
            ret += f"{sub} { 'adicionales' if i==0 else ''} "
            ret += f"{power}{' y' if last else ' ,'}"
            i+=1
        return f'{ret[:-2]}'

    @staticmethod
    def replaces(replacements):
        ret = ''
        for r in replacements:
            ret += f' {"Cualquier" if (r.count == 0) else "Un" if (r.count == 1) else r.count } {r.replacement.name}{"s" if r.count>1 else ""} puede reemplazar a un { r.troop.name }'
        return ret

    @staticmethod
    def equipmnt(equipment):
        return f'Cada miniatura está armada con { NaturalList([t.e.name for t in equipment]) }.'
        
    @staticmethod
    def redact(unit):
        def __get_units(crew):
            return [{'name' : c.troop.name, 'quantity' : c.quantity, 'cost' : c.cost, 'power' : c.power , 'alternative' : c.alternative } for c in crew]
        c = __get_units(unit.troops.all())
        o = __get_units(unit.opt_troops.all())
        r = unit.replacements.all()        
        e = unit.equipment.all()        
        return mark_safe(
            f'{DescriptionRedactor.contains(c)         }.'+
            f'{DescriptionRedactor.includes(o)      }.'+
            f'{DescriptionRedactor.replaces(r)  }.'+
            f'{DescriptionRedactor.equipmnt(e)  }.'+
            ''
        )
