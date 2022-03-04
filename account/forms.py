from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError

from account.models import Account
from account.constants import *

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

	class Meta:
		model = Account
		fields = ('email', 'identification', 'password1', 'password2', )

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_identification(self):
		identification = self.cleaned_data['identification']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(identification=identification)
		except Account.DoesNotExist:
			if len(identification) <= 12 :
				if identification not in NoBP_dict:
					raise forms.ValidationError('NoBP tidak valid')
			elif len(identification) > 12 :
				if identification not in NoBP_dict:
					raise forms.ValidationError('NIP tidak valid')
			return identification
		raise forms.ValidationError('NoBP/NIP "%s" is already in use.' % identification)

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(identification=email, password=password):
				raise forms.ValidationError("Invalid login")

class LoginAuthenticationForm(forms.Form):

	email = forms.CharField(max_length=50)
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):

				if '@' in email:
					user = get_user_model().objects.filter(email=email).first()
					if user:
						raise forms.ValidationError("Password Salah")
					else:
						raise forms.ValidationError("Tidak ada akun dengan email tersebut")
				elif email.isdecimal():
					user = get_user_model().objects.filter(identification=email).first()
					if user:
						raise forms.ValidationError("Password Salah")
					else:
						raise forms.ValidationError("Tidak ada akun dengan NoBP/NIP tersebut")

				raise forms.ValidationError("Invalid login")


