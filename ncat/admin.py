from ncat.models import Item, UserProfile, Comentarios
from django.contrib import admin

class ItemAdmin(admin.ModelAdmin):
	fields = ('titulo', 'criado', 'editado', 'descricao')
	list_display = ('criado', 'editado', 'titulo')

	def save_model(self, request, obj, form, change):
		obj.usuario = request.user
		obj.save()
		
	def queryset(self, request):
		qs = super(ItemAdmin, self).queryset(request)
		return qs.filter(usuario=request.user)

#class ComentariosAdmin(admin.ModelAdmin):
#	fields = ('post_id', 'papai_id', 'usuario', 'criado', 'editado', 	'comentario', 'up_votes', 'down_votes')
	
# admin.site.register(Item, ItemAdmin)
# admin.site.register(UserProfile)
# admin.site.register(Comentarios)

