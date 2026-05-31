import graphene
from graphene import relay, ObjectType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import *
from .views import Api

"""
###############################################################################
# WORKING
###############################################################################
"""
class GearNode(DjangoObjectType):
    class Meta:
        model = Gear
        fields = '__all__'
   
class GearStepNode(DjangoObjectType):
    class Meta:
        model = GearStep
        fields = '__all__'
        
class MaterialNode(DjangoObjectType):
    class Meta:
        model = Material
        fields = '__all__'

class MaterialStepNode(DjangoObjectType):
    class Meta:
        model= MaterialStep
        fields = '__all__'
        
class TaxonomyNode(DjangoObjectType):
    class Meta:
        model = Taxonomy
        fields = '__all__'

class SubtaxonomyNode(DjangoObjectType):
    class Meta:
        model = Subtaxonomy
        fields = '__all__'

class PictureNode(DjangoObjectType):
    class Meta:
        model = Picture
        fields = '__all__'
        
class PictureStepNode(DjangoObjectType):
    class Meta:
        model = Picture
        fields = '__all__'

"""
###############################################################################
# WORK IN PROGRESS
###############################################################################
"""



        

class ProjectNode(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'
        filter_fields = ['id', 'name']        
        interfaces = (relay.Node,)
        

class StepNode(DjangoObjectType):
    class Meta:
        model = Step
        fields = '__all__'
        filter_fields = ['id', 'brief_description', 'project']
        interfaces = (relay.Node,)
        

class SceniaQuery(graphene.ObjectType):
    gear                = graphene.Field(GearNode, gear_id=graphene.String())
    all_gear            = graphene.List(GearNode)
    gear_step           = graphene.Field(GearStepNode, gearstep_id=graphene.String(), step_id=graphene.Int(), gear_id=graphene.Int())
    all_gear_step       = graphene.List(GearStepNode)
    material            = graphene.Field(MaterialNode, material_id=graphene.String())
    all_material        = graphene.List(MaterialNode)
    material_step       = graphene.Field(MaterialNode, material_step_id=graphene.String())
    all_material_step   = graphene.List(MaterialStepNode)
    taxonomy            = graphene.Field(TaxonomyNode, taxonomy_id=graphene.String())
    all_taxonomy        = graphene.List(TaxonomyNode)
    subtaxonomy         = graphene.Field(SubtaxonomyNode, subtaxonomy_id=graphene.String())
    all_subtaxonomy     = graphene.List(SubtaxonomyNode)
    picture             = graphene.Field(PictureNode, picture_id=graphene.String())
    all_picture         = graphene.List(PictureNode)
    picture_step        = graphene.Field(PictureStepNode, picture_step_id=graphene.String())
    all_picture_step    = graphene.List(PictureStepNode)
    """
    step  = relay.Node.Field(GearNode)
    all_steps = DjangoFilterConnectionField(StepNode)
    project = relay.Node.Field(ProjectNode)
    all_projects = DjangoFilterConnectionField(ProjectNode)
    """

    def resolve_gear(self, info, gear_id):                  return Gear.objects.get(id=gear_id)
    def resolve_all_gear(self, info, **kwargs):             return Gear.objects.all()
    def resolve_gear_step(self, info, gear_step_id):        return GearStep.objects.get(id=gear_step_id)
    def resolve_all_gear_step(self, info, **kwargs):        return GearStep.objects.all()
    def resolve_material(self, info, material_id):          return Material.objects.get(id=material_id)
    def resolve_all_material(self, info, **kwargs):         return Material.objects.all()
    def resolve_material_step(self, info, material_step_id):return MaterialStep.objects.get(id=material_step_id)
    def resolve_all_material_step(self, info, **kwargs):    return MaterialStep.objects.all()
    def resolve_taxonomy(self, info, taxonomy_id):          return Taxonomy.objects.get(id=taxonomy_id)
    def resolve_all_taxonomy(self, info, **kwargs):         return Taxonomy.objects.all()
    def resolve_subtaxonomy(self, info, subtaxonomy_id):    return Subtaxonomy.objects.get(id=subtaxonomy_id)
    def resolve_all_subtaxonomy(self, info, **kwargs):      return Subtaxonomy.objects.all()
    def resolve_picture(self, info, picture_id):            return Picture.objects.get(id=picture_id)
    def resolve_all_picture(self, info, **kwargs):          return Picture.objects.all()
    
schema = graphene.Schema(query=SceniaQuery)