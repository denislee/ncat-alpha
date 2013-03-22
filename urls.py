from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', "ncat.views.lista"),
    (r'^adiciona/$', "ncat.views.adiciona"),
    
    (r'^c/(?P<nr_item>\d+)/$', "ncat.views.item"),
    
    (r'^c/(?P<nr_item>\d+)/editar/$', "ncat.views.item_editar"),	# edita o post (se voce for o dono, claro)
    (r'^c/(?P<nr_item>\d+)/comentar/(?P<nr_papai>\d+)$', "ncat.views.item_comentar"),	# comentar o post (se vc estiver logado)
    (r'^c/(?P<nr_item>\d+)/comentarios/$', "ncat.views.item_comentarios"),	# request para ver os comentarios do post

    (r'^c/(?P<nr_item>\d+)/up/$', "ncat.views.vote_up"),
    (r'^c/(?P<nr_item>\d+)/down/$', "ncat.views.vote_down"),

    (r'^c/(?P<nr_item>\d+)/up_c/$', "ncat.views.vote_up_c"),
    (r'^c/(?P<nr_item>\d+)/down_c/$', "ncat.views.vote_down_c"),

    (r'^remove/(?P<nr_item>\d+)/$', "ncat.views.remove"),
    
    (r'^login/', "django.contrib.auth.views.login", { 
    	"template_name": "login.html" }),
    (r'^logout/', "django.contrib.auth.views.logout_then_login", { 
    	"login_url": "/" }),    	

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    (r'^registrar/', "ncat.views.registrar"),

    (r'syncdb/$', "ncat.views.syncdb"), # atualizar a pontuacao dos posts/comentarios.    
    
    #jquery test
    (r'^jquery/', "ncat.views.jquery"),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT}),
	)
