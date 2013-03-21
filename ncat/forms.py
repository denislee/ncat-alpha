from django import forms
from models import Item, UserProfile, Comentarios

class FormItem(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('titulo', 'descricao')
	
		def save(self):
			if not self.id:
				self.criado = datetime.datetime.today()
			self.editado = datetime.datetime.today()
			super(FormItem, self).save()	

class FormComentarios(forms.ModelForm):
	class Meta:
		model = Comentarios
		fields = ('comentario',) #fields necessarios para validar o form
		
		def save(self):
			if not self.id:
				self.criado = datetime.datetime.today()
			self.editado = datetime.datetime.today()
			super(FormComentarios, self).save()

# create user form
class FormCreateUser(forms.Form):
	username = forms.CharField(max_length=30)
	email = forms.EmailField()
	password1=forms.CharField(max_length=30,widget=forms.PasswordInput()) #render_value=False
	password2=forms.CharField(max_length=30,widget=forms.PasswordInput())
	
	def save(self): # create new user
	    new_user=User.objects.create_user(username=self.cleaned_data['username'],
	                                    password1=self.cleaned_data['password'],
	                                    email=self.cleaned_data['email'],
	                                    )
	    return new_user

	def clean(self): # check if password 1 and password2 match each other
	    if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
	        if self.cleaned_data['password1'] != self.cleaned_data['password2']: # check if they match each other
	        	raise forms.ValidationError("passwords dont match each other")
	    return self.cleaned_data
		
