from django.contrib import admin
from .models import *
from django.conf import settings
from django.utils.html import mark_safe
from django.template.loader import render_to_string
        
admin.site.register(ColorTheme)
admin.site.register(Game)
admin.site.register(Stratagem)
admin.site.register(Army)
admin.site.register(Keyword)
admin.site.register(Faction)
admin.site.register(Element)
admin.site.register(TroopChange)
admin.site.register(OptionalRule)
admin.site.register(SpecialRule)
admin.site.register(Equipment)
admin.site.register(UnitEquipment)
admin.site.register(Transport)
admin.site.register(Ability)
admin.site.register(TroopSet)
admin.site.register(Unit)
admin.site.register(WeaponType)
admin.site.register(Weapon)

admin.site.register(TroopEquipment)

# admin.site.register(Option)
# admin.site.register(UnitOption)
# admin.site.register(UnitTroop)
# admin.site.register(UnitWeapon)
# admin.site.register(ArmyStratagem)
# admin.site.register(ArmyUnit)


#DEPRECATED

class TroopAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        try:
            html = mark_safe(render_to_string('troop.html', context = {'URL_ROOT': settings.URL_ROOT, 'troop' : obj, 't' : obj }))
        except: 
            html = "sin imagen"
        return html
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    list_display = ['image_tag', 'name','ws','bs','s','t','w','a','ld','sv']

admin.site.register(Troop, TroopAdmin)