from django.contrib import admin
from .models import Quest, UserQuestProgress

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal', 'start_date', 'end_date', 'rewards')
    search_fields = ('title',)

@admin.register(UserQuestProgress)
class UserQuestProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'quest', 'progress', 'completed', 'rewards_claimed')
    search_fields = ('user__username', 'quest__title')
    list_filter = ('completed', 'rewards_claimed')