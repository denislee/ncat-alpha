from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import ast, datetime

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []
        if isinstance(value, list):
            return value
        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class ItemAgenda(models.Model):
	criado = models.DateTimeField()
	editado = models.DateTimeField()
	titulo = models.CharField(max_length=100)
	descricao = models.TextField()
	usuario = models.ForeignKey(User)
	up_votes = models.IntegerField(default=0)
	down_votes = models.IntegerField(default=0)
	n_comentarios = models.IntegerField(default=0)	# numero de comentarios
	points = models.IntegerField(default=0)
	# participantes = models.ManyToManyField(User, related_name="item_participantes")
	
	def __unicode__(self):
		return u"%s - %s %s" % (self.titulo, self.criado, self.criado)
	
	# colocando timestamp automaticamente
	def save(self):
		if not self.id:
			self.criado = datetime.datetime.today()
		self.editado = datetime.datetime.today()
		super(ItemAgenda, self).save()

# tabelinha para os comentarios
class Comentarios(models.Model):
	post_id = models.ForeignKey(ItemAgenda)
	papai_id = models.IntegerField(default=0, blank=True)
	usuario = models.ForeignKey(User)
	comentario = models.TextField(max_length=500)
	criado = models.DateTimeField()
	editado = models.DateTimeField()
	up_votes = models.IntegerField(default=0, blank=True)
	down_votes = models.IntegerField(default=0, blank=True)
	points = models.IntegerField(default=0)
	def __unicode__(self):
		return u"%s - %s %s" % (self.usuario, self.criado, self.criado)

	# colocando timestamp automaticamente
	def save(self):
		if not self.id:
			self.criado = datetime.datetime.today()
			up_votes = 0
			down_votes = 0
		self.editado = datetime.datetime.today()
		super(Comentarios, self).save()

class UserProfile(models.Model):  
	user = models.OneToOneField(User)
	up_voted = ListField()
	down_voted = ListField()
	up_voted_c = ListField() # comentarios
	down_voted_c = ListField() # comentarios
	def __str__(self):  
		return "%s's profile" % self.user  

def create_user_profile(sender, instance, created, **kwargs):  
	if created:  
		profile, created = UserProfile.objects.get_or_create(user=instance)  
post_save.connect(create_user_profile, sender=User) 


