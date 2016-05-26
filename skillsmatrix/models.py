from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Skill model
class Skill(models.Model):
    name = models.CharField(max_length=512)
    difficulty = models.IntegerField()
    family = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name


# Developer model
class Developer(models.Model):
    user = models.OneToOneField(User)
    extra_credit_tokens = models.IntegerField(default=0)
    manager = models.CharField(max_length=30)
    title = models.CharField(max_length=30)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


# DeveloperSkill model
class DeveloperSkill(models.Model):
    developer = models.ForeignKey('Developer', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    proficiency = models.CharField(max_length=30)
    years_of_experience = models.IntegerField()

    def __unicode__(self):
        return u'%s %s' % (self.developer, self.skill)


# ExtraCredit model
class ExtraCredit(models.Model):
    recipient = models.ForeignKey(Developer, related_name='extracredit_recipient')
    sender = models.ForeignKey(Developer, related_name='extracredit_sender')
    skill = models.ForeignKey(Skill, related_name='extracredit_skill')
    description = models.TextField(blank=True, null=True)
    date_credited = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s %s -> %s %s - %s' % (self.sender.user.first_name, self.recipient.user.last_name, self.recipient.user.first_name, self.recipient.user.last_name, self.skill.name)