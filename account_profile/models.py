from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from account.constants import NoBP_dict

from account.models import Account
from account.backends import *

from post.models import rand_slug

class AccountProfile(models.Model):
	account = models.OneToOneField(Account, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
	fullname = models.CharField(max_length=100, blank=True, null=True)
	is_direktur = models.BooleanField(default=False)
	is_dosen = models.BooleanField(default=False)
	is_mahasiswa = models.BooleanField(default=False)
	badge = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.fullname

	def toDosen(self):
		self.is_dosen = True
		self.save()
	
	def toMahasiswa(self):
		self.is_mahasiswa = True
		self.save()
	
	def save(self, *args, **kwargs):
		if len(self.account.identification) == 10:
			self.is_mahasiswa = True
		else:
			self.is_dosen = True
		
		if self.is_mahasiswa:
			try:
				self.fullname = NoBP_dict[self.account.identification]
			except:
				random = rand_slug()
				self.fullname = "MHS " + random
		else:
			try:
				self.fullname = NIP_dict[self.account.identification]
			except:
				random = rand_slug()
				self.fullname = "DSN " + random
		super(AccountProfile, self).save(*args, **kwargs)


@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		AccountProfile.objects.create(account=instance)


