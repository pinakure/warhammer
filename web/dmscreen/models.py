from django.db.models.fields.related    import ForeignKey
from django.template.loader             import render_to_string
from django.utils.html                  import mark_safe
from django.conf                        import settings
from django.db                          import models
from .common                            import *

class ColorTheme(models.Model):
    bg_nav          = models.CharField(max_length=256, default = "#000")
    fg_nav          = models.CharField(max_length=256, default = "#ffff00e0")
    bg_icon         = models.CharField(max_length=256, default = "#6A769988")
    fg_icon         = models.CharField(max_length=256, default = "#ffffffa0")
    bg_caption      = models.CharField(max_length=256, default = "#000")
    fg_caption      = models.CharField(max_length=256, default = "#ffffff")
    bg_tab          = models.CharField(max_length=256, default = "#ffff2040")
    fg_tab          = models.CharField(max_length=256, default = "#00000060")
    bg_thead        = models.CharField(max_length=256, default = "#fff0f06")
    fg_thead        = models.CharField(max_length=256, default = "#000")
    bg_table_odd    = models.CharField(max_length=256, default = "#ffff")
    fg_table_odd    = models.CharField(max_length=256, default = "#000")
    bg_table_even   = models.CharField(max_length=256, default = "#fffa")
    fg_table_even   = models.CharField(max_length=256, default = "#000")

    def __str__(self):
        fields = ColorTheme._meta.local_fields
        field_names = [f.name for f in fields]
        html = ''
        for k in field_names:
            if k == 'id':
                html +=f'<div style="display: inline-block">{self.id}</div>'
                continue
            html = mark_safe(f'{html}<div title="{k}"style="display: inline-block;width: 16px; height: 16px; border: 1px solid #fffa; border-radius: 3px 3px 3px 3px; background-color: {eval(f"self.{k}")};"></div>')
        return html

class Game(models.Model):
    name        = models.CharField(max_length=16)
    title       = models.CharField(max_length=32)
    picture     = models.ImageField(null=True, blank=True)
    
    def __str__(self):    return f'{self.title}'
    def json(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'title'         : self.title,
            'picture'       : self.picture.url if self.picture else '',
        }

class Stratagem(models.Model):
    title       = models.CharField(primary_key=True, max_length=64)
    narrative   = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cost        = models.IntegerField('PM Needed')
    cost_alt    = models.IntegerField('PM Needed for alternatives / Recast')
    
    def __str__(self): return f'{ self.title }'
    def json(self, army='None'):
        cost = f'{ self.cost }PM'
        if self.cost_alt > 0:
            cost = cost + f' / { self.cost_alt }PM'
        return {
            'name'        : self.title,
            'title'       : self.title,
            'narrative'   : mark_safe(self.narrative),
            'description' : mark_safe(self.description),
            'cost'        : cost,            
            'army'        : army,
        }

class Army(models.Model):
    name        = models.CharField(max_length=32)
    game        = models.ForeignKey('Game', on_delete=models.CASCADE)
    font        = models.CharField(max_length=32, default='Times new Roman')
    picture     = models.ImageField(null=True, blank=True)
    stratagems  = models.ManyToManyField("Stratagem", blank=True)

    def __str__(self):
        return mark_safe(f'''
                <div style="display: inline-block; text-align: center">
                    <img src="{settings.URL_ROOT}/{self.picture.url      if self.picture else ""}" style="border-radius: 5px 5px 5px 5px; height: auto; width: 200px;"/>
                    <div style="display: inline-block; text-align: left; position: relative;">
                        <img src="{settings.URL_ROOT}/{self.game.picture.url if self.game and self.game.picture else ""}" style="filter: opacity(50%); height: 32px; width: auto;"/><br/>
                        <span style="font-size: 32px">{self.name}</span>
                    </div>
                </div>
            ''')
    def json(self):
        return {
            'id'          : self.id,
            'name'        : self.name,
            'game'        : self.game,
            'font'        : self.font,
            'picture'     : self.picture,
            'stratagems'  : [ o.json() for o in self.stratagems.all() ],
        }

class Keyword(models.Model):
    keyword     = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True, default='-')

    def __str__(self): return f'{self.keyword}'
    def printable(self): return f'<p><b title="{self.description}"">{self.keyword}</b></p>'
    def json(self):
        return {
            'id'            : self.id,
            'keyword'       : self.keyword,
            'description'   : self.description
        }
    
class Faction(models.Model):
    name        = models.CharField(max_length=64)
    description = models.TextField(default="This Faction has no description.")
    keywords    = models.ManyToManyField('Keyword', blank=True)

    def __str__(self): return f'{self.name}'
    def json(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'description'   : self.description,
            'keywords'      : " ".join([o.keyword for o in self.keywords.all() ]),
        }

class Element(models.Model):
    name        = models.CharField(max_length=64)
    description = models.TextField(default="This Element has no description.")
    
    def __str__(self): return f'{self.name}'
    def printable(self): return f'<p><b>{self.name}</b>:<span style="font-weight: 100">{self.description}</span></p>'
    def json(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'description'   : self.description,
        }

class TroopChange(models.Model):
    troop       = models.ForeignKey('Troop', verbose_name="Previous Troop"  , related_name="before", on_delete=models.CASCADE)
    replacement = models.ForeignKey('Troop', verbose_name="New Troop"       , related_name="after" , on_delete=models.CASCADE)
    cost        = models.IntegerField("Replacement cost", default=0)
    count       = models.IntegerField("Number of Replacements allowed", default=1)

    def __str__(self): return f'{self.troop.name} -> {self.replacement.name} x {self.count} ({self.cost})'
    def json(self):
        return {
            'id'            : self.id,
            'troop'         : self.troop.json(),
            'replacement'   : self.replacement.json(),
            'cost'          : self.cost,
            'count'         : self.count,
        }

class OptionalRule(models.Model):
    name        = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    cost        = models.IntegerField(default=0)
    per_mini    = models.BooleanField("Cost per miniature", default=False)

    def __str__(self): return f'{self.name} ({self.cost}{ f" x mini" if self.per_mini else ""})'
    def printable(self): return f'<p><b>{self.name}</b>:<span style="font-weight: 100">{self.description}</span><i>{"" if self.cost==0 else f" ({self.cost} pts.)"}</i></p>'
    def json(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'description'   : self.description,
            'cost'          : self.cost,
            'per_mini'      : 1 if self.per_mini else 0,
        }

class SpecialRule(models.Model):
    name        = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)

    def __str__(self): return f'{self.name}'
    def printable(self): return f'<p><b title="{self.description}">{self.name}</b></p>'
    def json(self): 
        return {
            'id'            : self.id,
            'name'          : self.name,
            'description'   : self.description,
        }

class Equipment(models.Model):
    name        = models.CharField("Equipment Name", max_length=64)
    description = models.TextField("Narrative description", max_length=256, blank=True)
    rules       = models.TextField("Rules", max_length=256, blank=True)
    cost        = models.IntegerField("Generic Point Cost", default=1)
    
    def __str__(self): return f'{self.name} ({ self.cost } pt)'
    def json(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'description'   : self.description,
            'rules'         : self.rules,
            'cost'          : self.cost,
        }

class UnitEquipment(models.Model):
    e           = ForeignKey("Equipment", verbose_name="Equipment"  , related_name="ue", on_delete=models.CASCADE)
    cost        = models.IntegerField("Cost override", default=None, null=True, blank=True)

    def __int__(self): return self.id
    def __str__(self): return f'{self.e.name} ({ self.get_cost() } pt)'
    def get_cost(self): return self.cost if self.cost is not None else self.e.cost
    def json(self):
        return {
            'id'            : self.id,
            'description' : self.e.name,
            'equipment'   : self.e.json(),
            'cost'        : self.get_cost(),
        }
    
class Transport(models.Model):
    name        = models.CharField(max_length=64)

    def __str__(self): return self.name

class Ability(models.Model):
    name        = models.CharField(max_length=64)
    description = models.TextField()
    
    def __str__(self):   return self.name
    def printable(self): return f'<p><b>{self.name}</b>:<span style="font-weight: 100">{self.description}</span></p>'
    def json(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'description'   : self.description,
        }

class TroopSet (models.Model):
    troop       = models.ForeignKey("Troop", on_delete=models.CASCADE)
    quantity    = models.IntegerField(default=1)
    cost        = models.IntegerField("Cost per mini", default=1)
    power       = models.IntegerField("Power added to the unit if this option is taken", default=1)
    alternative = models.BooleanField("True if this an alternative to another troopset", default=False)

    def __str__(self): return f'{self.troop.name} x {self.quantity} ({self.cost})'
    def json(self):
        return {
            'id'            : self.id,
            'troop'         : self.troop.json(),
            'quantity'      : self.quantity,
            'cost'          : self.cost,
            'alternative'   : 1 if self.alternative else 0,
        }

class Unit(models.Model):
    army        = models.ForeignKey('Army', default=None, on_delete=models.CASCADE, null=True, blank=True)
    title       = models.CharField(max_length=64)
    subtitle    = models.CharField(max_length=64, null=True, blank=True)
    faction     = models.ForeignKey('Faction', on_delete=models.SET_NULL, null=True)
    element     = models.ForeignKey('Element', on_delete=models.SET_NULL, null=True)
    power       = models.IntegerField(default=5)
    keywords    = models.ManyToManyField('Keyword'      , verbose_name="Unit Keywords"      , related_name="keywords"       , blank=True)
    troops      = models.ManyToManyField('TroopSet'     , verbose_name="Troop Composition"  , related_name='troops'         , blank=True)
    opt_troops  = models.ManyToManyField('TroopSet'     , verbose_name="Optional Troops"    , related_name='opt_troops'     , blank=True)
    opt_rules   = models.ManyToManyField('OptionalRule' , verbose_name="Optional Rules"     , related_name='opt_rules'      , blank=True)
    specialrules= models.ManyToManyField('SpecialRule'  , verbose_name="Special Rules"      , related_name='specialrules'   , blank=True)
    equipment   = models.ManyToManyField('UnitEquipment', verbose_name="Unit Equipment"     , related_name='unitequipment'  , blank=True)
    abilities   = models.ManyToManyField('Ability'      , verbose_name="Unit Abilities"     , related_name='abilities'      , blank=True)
    replacements= models.ManyToManyField('TroopChange'  , verbose_name="Troop Replacements" , blank=True)
    transport   = models.ForeignKey('Transport', on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):return f'[{self.army.name if self.army else "UNALIGNED"}] {self.title}'
    
    def _get_weapons(self):
        weapons = set()
        for t in self.troops.all():
            for w in t.troop.weapons.all():
                weapons.add(w)
        for t in self.opt_troops.all():
            for w in t.troop.weapons.all():
                weapons.add(w)
        for t in self.replacements.all():
            for w in t.replacement.weapons.all():
                weapons.add(w)
        return [ w.json() for w in weapons]
        
    def _get_crew(self):
        """ Retrieves the set of data to be dislayed on the datacard troop section """
        troops = set()
        for t in self.troops.all(): troops.add(t.troop)
        for t in self.opt_troops.all(): troops.add(t.troop)
        for t in self.replacements.all(): troops.add(t.replacement)
        return [ t.json() for t in troops]

    def _get_troop_keywords(self):
        keywords = []
        for t in self.troops.all():     keywords.append({ 'troop' : t.troop.name, 'keywords' : [ o.keyword for o in t.troop.keywords.all()] })
        for t in self.opt_troops.all(): keywords.append({ 'troop' : t.troop.name, 'keywords' : [ o.keyword for o in t.troop.keywords.all()] })
        return keywords

    def json(self):
        troops           = [ o.json() for o in self.troops.all() ]
        opt_troops       = [ o.json() for o in self.opt_troops.all() ]
        opt_rules        = [ o.json() for o in self.opt_rules.all() ]
        opt_replacements = [ o.json() for o in self.replacements.all() ]
        return {
            'id'              : self.id,
            'title'           : self.title,
            'subtitle'        : self.subtitle,
            'description'     : DescriptionRedactor.redact(self),
            'picture'         : 'deprecated',
            'faction'         : self.faction.name, 
            'faction_keywords': [ o.keyword for o in self.faction.keywords.all()],
            'keywords'        : self._get_troop_keywords(),
            'crew'            : self._get_crew(),
            'weapons'         : self._get_weapons(),
            'abilities'       : mark_safe('<div style="columns: 2">' + (  ''.join([ o.printable() for o in self.abilities.all()])  )+'</div>'),
            'equipment'       : [ o.json() for o in self.equipment.all()],
            'power'           : self.power,
            'element'         : self.element,
            'troops'          : troops,
            'opt_troops'      : opt_troops,
            'opt_rules'       : opt_rules,
            'replacements'    : opt_replacements,
            'transport'       : self.transport.name if self.transport else '',
        }

class WeaponType(models.Model):
    name        = models.CharField(max_length=64)
    description = models.TextField(default="This WeaponType has no description")

    def __str__(self):return self.name
    def json(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'description'   : self.description,
        }
    
class Weapon(models.Model):
    name        = models.CharField(max_length=64)
    range       = models.IntegerField(default=10)
    types       = models.ManyToManyField(WeaponType, related_name="weapontype", blank=True)
    picture     = models.ImageField(null=True, blank=True)
    s           = models.IntegerField(default=5, null=True, blank=True)
    ap          = models.IntegerField(default=5, null=True, blank=True)
    d           = models.CharField(max_length=5, default='', blank=True)
    abilities   = models.TextField(default="--")
    type        = models.ForeignKey('WeaponType', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):  return render_to_string('weapon.html', context={ 'weapon' : self })
    def json(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'range'         : self.range,
            'type'          : self.type.name,
            's'             : self.s,
            'ap'            : self.ap,
            'd'             : self.d,
            'abilities'     : mark_safe(self.abilities),
            'picture'       : self.picture,
        }

class TroopEquipment(models.Model):
    e           = ForeignKey("Equipment", verbose_name="Equipment"  , related_name="te", on_delete=models.CASCADE)
    t           = ForeignKey("Troop"    , verbose_name="Troop"      , related_name="tt", on_delete=models.CASCADE)
    cost        = models.IntegerField("Cost override", default=None, null=True, blank=True)

    def __int__(self): return self.id
    def __str__(self): return f'{self.t.name} -> {self.e.name} ({ self.get_cost() } pt)'
    def get_cost(self): return self.cost if self.cost is not None else self.e.cost

    def json(self):
        return {
            'equipment' : self.e.json(),
            'troop'     : self.t.name,
            'cost'      : self.get_cost(),
        }

class Troop(models.Model):
    name        = models.CharField("Troop Name", max_length=64)
    i           = models.IntegerField(" M/I  (Movimiento)", default=5)
    ws          = models.IntegerField("WS/HA (H.Armas)", default=5)
    bs          = models.IntegerField("BS/HP (H.Proyectiles)", default=5)
    s           = models.IntegerField(" S/F  (Fuerza)", default=5)
    t           = models.IntegerField(" T/R  (Resistencia)", default=5)
    w           = models.IntegerField(" W/H  (Heridas)", default=5)
    a           = models.IntegerField("  A   (Ataques)", default=5)
    ld          = models.IntegerField("  L   (Liderazgo)", default=5)
    sv          = models.IntegerField("  S   (Salvacion)", default=5)
    weapons     = models.ManyToManyField('Weapon'        , blank=True)
    equipment   = models.ManyToManyField('TroopEquipment', blank=True)
    abilities   = models.ManyToManyField('Ability'       , blank=True)
    picture     = models.ImageField(null=True, blank=True)
    keywords    = models.ManyToManyField('Keyword'       , blank=True)
    
    def __str__(self): return f'{self.name}'
    def json(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'movement'      : self.i,
            'ws'            : self.ws,
            'bs'            : self.bs,
            's'             : self.s,
            't'             : self.t,
            'i'             : self.i,
            'w'             : self.w,
            'a'             : self.a,
            'ld'            : self.ld,
            'sv'            : self.sv,
            'picture'       : self.picture if self.picture else '',
            'weapons'       : [ o.json() for o in self.weapons.all() ],
            'keywords'      : [ o.json() for o in self.keywords.all() ],
            'equipment'     : [ o.json() for o in self.equipment.all() ],
            'abilities'     : [ o.json() for o in self.abilities.all() ],
        }
        