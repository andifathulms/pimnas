from django.db import models
from django_editorjs import EditorJsField

from account.models import Account

class Group(models.Model):
    TYPES = (
        ('1', 'UKM'),
        ('2', 'HIMA'),
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPES)
    members = models.ManyToManyField(Account, blank=True, related_name='members')
    admins = models.ManyToManyField(Account, blank=True, related_name='admins')
    pembina = models.ManyToManyField(Account, blank=True, related_name='pembina')
    about = EditorJsField()
    achievement = EditorJsField()
    agenda = EditorJsField()
    struktur = EditorJsField()

    def __str__(self):
        return self.name

    def give_privilege(self, acc1, acc2):
        if self.is_admin(acc1):
            self.admins.add(acc2)
            self.members.remove(acc2)
            self.save()

    def take_privilage(self, acc1, acc2):
        if self.is_admin(acc1):
            self.admins.remove(acc2)
            self.members.add(acc2)
            self.save
    
    def is_admin(self, acc):
        if acc in self.admins.all():
            return True
        return False