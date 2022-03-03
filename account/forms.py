from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


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

	def clean_username(self):
		identification = self.cleaned_data['identification']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(identification=identification)
		except Account.DoesNotExist:
			return identification
		raise forms.ValidationError('NoBP/NIP "%s" is already in use.' % identification)

class AccountAuthenticationForm(forms.ModelForm): # CHANGE THIS

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