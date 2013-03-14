from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', "agenda.views.lista"),
    (r'^adiciona/$', "agenda.views.adiciona"),
    
    (r'^c/(?P<nr_item>\d+)/$', "agenda.views.item"),
    
    (r'^c/(?P<nr_item>\d+)/editar/$', "agenda.views.item_editar"),	# edita o post (se voce for o dono, claro)
    (r'^c/(?P<nr_item>\d+)/comentar/(?P<nr_papai>\d+)$', "agenda.views.item_comentar"),	# comentar o post (se vc estiver logado)
    (r'^c/(?P<nr_item>\d+)/comentarios/$', "agenda.views.item_comentarios"),	# request para ver os comentarios do post

    (r'^c/(?P<nr_item>\d+)/up/$', "agenda.views.vote_up"),
    (r'^c/(?P<nr_item>\d+)/down/$', "agenda.views.vote_down"),

    (r'^c/(?P<nr_item>\d+)/up_c/$', "agenda.views.vote_up_c"),
    (r'^c/(?P<nr_item>\d+)/down_c/$', "agenda.views.vote_down_c"),

    (r'^remove/(?P<nr_item>\d+)/$', "agenda.views.remove"),
    
    #(r'^login/', "django.contrib.auth.views.login"),
    (r'^login/', "django.contrib.auth.views.login", { 
    	"template_name": "login.html" }),
    (r'^logout/', "django.contrib.auth.views.logout_then_login", { 
    	"login_url": "/" }),    	
#    (r'^logout/', "django.contrib.auth.views.logout_then_login", { 
#    	"login_url": "/login/" }),    	
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    #registro de usuario
    (r'^registrar/', "agenda.views.registrar"),

    (r'syncdb/$', "agenda.views.syncdb"), # atualizar a pontuacao dos posts/comentarios.    
    #jquery test
    (r'^jquery/', "agenda.views.jquery"),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT}),
	)
