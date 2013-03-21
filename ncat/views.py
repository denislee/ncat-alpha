# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import datetime

# para registrar
from django.contrib.auth.models import User
from settings import SECRET_KEY
# os outros itens
from models import Item, UserProfile, Comentarios
from forms import FormItem, FormCreateUser, FormComentarios
# para o captcha
#captcha from captcha import Captcha
#captcha import Image, sha, string
import sha, string
# para redirecionar para a pagina anterior
from urlparse import urlsplit
#from urlparse import urlparse

def jquery(request):
	return render_to_response("jquery2.html", {},
		context_instance=RequestContext(request))

def lista(request):
	now = datetime.datetime.now()
	try:
		voteuser = get_object_or_404(UserProfile, user=request.user)
	except:
		voteuser = UserProfile()
		voteuser.up_voted = []
		voteuser.down_voted = []
		lista_itens = Item.objects.filter()[:10]
		return render_to_response("lista.html", {'lista_itens':lista_itens, 'voteuser':voteuser, 'current_date': now},
			context_instance=RequestContext(request))
	lista_itens = Item.objects.filter()[:10]
	return render_to_response("lista.html", {'lista_itens':lista_itens, 'voteuser':voteuser, 'current_date': now},
		context_instance=RequestContext(request))

def item_comentarios(request, nr_item):
	try:
		voteuser_c = get_object_or_404(UserProfile, user=request.user)
	except:
		voteuser_c = UserProfile()
		voteuser_c.up_voted_c = []
		voteuser_c.down_voted_c = []
		lista_comentarios = Comentarios.objects.filter(post_id=nr_item)[:10]
		return render_to_response("item_comentarios.html", {'lista_comentarios':lista_comentarios, 'voteuser_c':voteuser_c, 'nr_item':nr_item},
			context_instance=RequestContext(request))
	lista_comentarios = Comentarios.objects.filter(post_id=nr_item)[:10]
	return render_to_response("item_comentarios.html", {'lista_comentarios':lista_comentarios, 'voteuser_c':voteuser_c, 'nr_item':nr_item},
		context_instance=RequestContext(request))

@login_required	
def item_comentar(request, nr_item, nr_papai):
	if request.method == "POST":

		form = FormComentarios(request.POST, request.FILES)

		if form.is_valid():
			item = form.save(commit=False)
			
			post = get_object_or_404(Item, pk=nr_item) # contador de comentarios
			post.n_comentarios = post.n_comentarios + 1	     # contador de comentarios
			post.save()

			item.usuario = request.user
			item.post_id = post
			item.papai_id = nr_papai

			item.up_votes = 0
			item.down_votes = 0

			item.save()
			form.save_m2m()
			
		#	referer = request.META.get('HTTP_REFERER', None)
			return render_to_response("salvo.html", {})
		else:
			print form.errors
			form = FormComentarios()
			return render_to_response("item_comentar.html", {'form': form, 'papai': nr_papai},
				context_instance=RequestContext(request))			
	else:
		form = FormComentarios()
		return render_to_response("item_comentar.html", {'form': form, 'papai': nr_papai},
			context_instance=RequestContext(request))

@login_required
def adiciona(request):
	if request.method == "POST":

		form = FormItem(request.POST, request.FILES)
		data = request.POST.copy()
		SALT = SECRET_KEY[:20]
        
		print '- conferindo ---------------------------------------'
		print data
		print data['hash_code_captcha']
		print sha.new(SALT+data['imgtext']).hexdigest()

#captcha		if (form.is_valid() and data['hash_code_captcha'] == sha.new(SALT+string.upper(data['imgtext'])).hexdigest() ):
		if form.is_valid():

			item = form.save(commit=False)
			item.usuario = request.user
			
			# tentando ja colocar um up vote
			#item.up_votes = 1
			#voteuser = get_object_or_404(UserProfile, user=request.user)
			#voteuser.up_voted.append(nr_item)
			#voteuser.save()
			
			item.save()
			form.save_m2m()
			return HttpResponseRedirect("/")
#			return render_to_response("salvo.html", {})
		else:
#captcha			c = Captcha()
#captcha			dados = c.gerarImagem(request.META['REMOTE_ADDR'])
			form = FormItem()
#captcha			return render_to_response("adiciona.html", {'form': form, 'dados': dados, 'data': data},
			return render_to_response("adiciona.html", {'form': form},
				context_instance=RequestContext(request))			
	else:
#captcha		c = Captcha()
#captcha		dados = c.gerarImagem(request.META['REMOTE_ADDR'])
		form = FormItem()
#captcha		return render_to_response("adiciona.html", {'form': form, 'dados': dados},
		return render_to_response("adiciona.html", {'form': form},
			context_instance=RequestContext(request))

def item(request, nr_item):
	try:
		voteuser = get_object_or_404(UserProfile, user=request.user)
	except:
		voteuser = UserProfile()
		voteuser.up_voted = []
		voteuser.down_voted = []
		item = get_object_or_404(Item, pk=nr_item)
		return render_to_response("item.html", {'item':item, 'voteuser':voteuser},
			context_instance=RequestContext(request))
	item = get_object_or_404(Item, pk=nr_item)
	return render_to_response("item.html", {'item':item, 'voteuser':voteuser},
		context_instance=RequestContext(request))

@login_required	
def item_editar(request, nr_item):
	item = get_object_or_404(Item, pk=nr_item, usuario=request.user)

	if request.method == "POST":
		form = FormItem(request.POST, request.FILES, instance=item)
		if form.is_valid():
			item = form.save(commit=False)
			item.usuario = request.user
			item.save()
			form.save_m2m()
			return render_to_response("salvo.html", {})
	else:
		form = FormItem(instance=item) #se o usuario for dono, edita; caso contrário, não edita
		return render_to_response("item_editar.html", {'form': form, 'item': item},
						context_instance=RequestContext(request))

	item = get_object_or_404(Item, pk=nr_item)
	return render_to_response("item.html", {'item': item},
	context_instance=RequestContext(request))

@login_required	
def remove(request, nr_item):
	item = get_object_or_404(Item, pk=nr_item, usuario=request.user)
	if request.method == "POST":
		item.delete()
		return render_to_response("removido.html", {})
	return render_to_response("remove.html", {'item': item},
		context_instance=RequestContext(request))

def registrar(request):
	if request.method == "POST":

		form = FormCreateUser(request.POST, request.FILES)
		data = request.POST.copy()
		SALT = SECRET_KEY[:20]

		print '- conferindo ---------------------------------------'
		print data['imgtext']

#captcha		if (form.is_valid() and
#captcha	     data['hash_code_captcha'] == sha.new(SALT+string.upper(data['imgtext'])).hexdigest() ):
		if form.is_valid():
			user = User.objects.create_user(form.cleaned_data['username'], 
					form.cleaned_data['email'], form.cleaned_data['password1'])
			user.is_staff = True
			user.save()
			return render_to_response("criado.html", {})
		else:
			form = FormCreateUser()
#captcha			c = Captcha()
#captcha			dados = c.gerarImagem(request.META['REMOTE_ADDR'])
#captcha			return render_to_response("registrar.html", {'form': form, 'dados': dados, 'data':data},
			return render_to_response("registrar.html", {'form': form},
				context_instance=RequestContext(request))
	else:
		form = FormCreateUser()
#captcha		c = Captcha()
#captcha		dados = c.gerarImagem(request.META['REMOTE_ADDR'])
#captcha		return render_to_response("registrar.html", {'form': form, 'dados': dados},
		return render_to_response("registrar.html", {'form': form},
					context_instance=RequestContext(request))

@login_required	
def vote_up(request, nr_item):

	item = get_object_or_404(Item, pk=nr_item)
	voteuser = get_object_or_404(UserProfile, user=request.user)
	
	if voteuser.up_voted.count(nr_item) > 0:
		return render_to_response("votado.html", {'item': item},
			context_instance=RequestContext(request))
	else:
		item.up_votes = item.up_votes + 1
		voteuser.up_voted.append(nr_item)
		if voteuser.down_voted.count(nr_item) > 0:
			voteuser.down_voted.remove(nr_item)
			item.down_votes = item.down_votes - 1
		item.save()
		voteuser.save()
	return render_to_response("votado.html", {'item': item},
		context_instance=RequestContext(request))

@login_required	
def vote_down(request, nr_item):

	item = get_object_or_404(Item, pk=nr_item)
	voteuser = get_object_or_404(UserProfile, user=request.user)
	
	if voteuser.down_voted.count(nr_item) > 0:
		return render_to_response("votado.html", {'item': item},
			context_instance=RequestContext(request))
	else:
		item.down_votes = item.down_votes + 1
		voteuser.down_voted.append(nr_item)
		if voteuser.up_voted.count(nr_item) > 0:
			voteuser.up_voted.remove(nr_item)
			item.up_votes = item.up_votes - 1
		voteuser.save()
		item.save()
	return render_to_response("votado.html", {'item': item},
		context_instance=RequestContext(request))

# para os comentarios.
@login_required	
def vote_up_c(request, nr_item):

	item = get_object_or_404(Comentarios, pk=nr_item)
	voteuser = get_object_or_404(UserProfile, user=request.user)
	
	if voteuser.up_voted_c.count(nr_item) > 0:
		return render_to_response("votado.html", {'item': item},
			context_instance=RequestContext(request))
	else:
		item.up_votes = item.up_votes + 1
		voteuser.up_voted_c.append(nr_item)
		if voteuser.down_voted_c.count(nr_item) > 0:
			voteuser.down_voted_c.remove(nr_item)
			item.down_votes = item.down_votes - 1
		item.save()
		voteuser.save()
	return render_to_response("votado.html", {'item': item},
		context_instance=RequestContext(request))

@login_required	
def vote_down_c(request, nr_item):

	item = get_object_or_404(Comentarios, pk=nr_item)
	voteuser = get_object_or_404(UserProfile, user=request.user)
	
	if voteuser.down_voted_c.count(nr_item) > 0:
		return render_to_response("votado.html", {'item': item},
			context_instance=RequestContext(request))
	else:
		item.down_votes = item.down_votes + 1
		voteuser.down_voted_c.append(nr_item)
		if voteuser.up_voted_c.count(nr_item) > 0:
			voteuser.up_voted_c.remove(nr_item)
			item.up_votes = item.up_votes - 1
		voteuser.save()
		item.save()
	return render_to_response("votado.html", {'item': item},
		context_instance=RequestContext(request))

def syncdb(request):

	return render_to_response('syncdb.html',{},
		context_instance=RequestContext(request))



