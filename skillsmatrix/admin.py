from django.contrib import admin
from skillsmatrix.models import Skill, Developer, DeveloperSkill, ExtraCredit


# Skill admin configuration
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'family')
    list_filter = ('difficulty', 'family')

admin.site.register(Skill, SkillAdmin)


# Developer admin configuration
admin.site.register(Developer)


# DeveloperSkills admin configuration
class DeveloperSkillAdmin(admin.ModelAdmin):
    list_display = ('developer', 'skill', 'proficiency', 'years_of_experience')
    list_filter = ('skill', 'proficiency', 'years_of_experience')

    def get_developer_username(self, obj):
        return obj.developer.user.username

    get_developer_username.short_description = 'Developer Username'

admin.site.register(DeveloperSkill, DeveloperSkillAdmin)


# ExtraCredit admin configuration
admin.site.register(ExtraCredit)


