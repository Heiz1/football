from django.contrib import admin
from .models import Teams,Scores,GameInfo,Groups
# Register your models here.

@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('team','group')


@admin.register(Scores)
class ScoresAdmin(admin.ModelAdmin):
    list_display = ('team','group','score','goal',
    'lost','goal_difference')


@admin.register(GameInfo)
class GameInfoAdmin(admin.ModelAdmin):
    list_display = ('id','time','HomeTeam',
    'HomeTeam_score','VisitingTeams_score','VisitingTeams')


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('group',)