from django.contrib import admin
from .models import User,SkillPost,SkillCategory,Skill
# Register your models here.

admin.site.register(User)
admin.site.register(SkillPost)
admin.site.register(SkillCategory)
admin.site.register(Skill)
