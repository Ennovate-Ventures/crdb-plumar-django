from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Talent)
admin.site.register(Education)
admin.site.register(Award)
admin.site.register(Skill)
admin.site.register(Experience)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizQuestionAnswer)
admin.site.register(TalentQuiz)
admin.site.register(TalentQuizAnswer)
