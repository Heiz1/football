from django.db import models

# Create your models here.

# 分组
class Groups(models.Model):
    group = models.CharField(max_length=10,verbose_name='小组')
    
    def __str__(self):
        return self.group

# 队伍
class Teams(models.Model):
    team = models.CharField(max_length=30,verbose_name='球队')
    group = models.ForeignKey(Groups,on_delete=models.DO_NOTHING)
    
    
    def __str__(self):
        return self.team

# 积分榜
class Scores(models.Model):
    team = models.ForeignKey(Teams,on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Groups,on_delete=models.DO_NOTHING)

    goal = models.CharField(max_length=20,verbose_name='进球')
    lost = models.CharField(max_length=20,verbose_name='失球')
    goal_difference = models.CharField(max_length=20,verbose_name='净胜球')
    score = models.CharField(max_length=20,verbose_name='积分')

    def __str__(self):
        return str(self.team)

    class Meta:
        ordering = ['-score','-goal_difference','team_id']



# 比赛情况
class GameInfo(models.Model):
    groups = models.ForeignKey(Groups,on_delete=models.DO_NOTHING)
    HomeTeam = models.ForeignKey(Teams,related_name='HomeTeam',on_delete=models.DO_NOTHING)
    VisitingTeams = models.ForeignKey(Teams,related_name='VisitingTeam',on_delete=models.DO_NOTHING)
    HomeTeam_score = models.CharField(max_length=20,verbose_name='主队进球')
    VisitingTeams_score = models.CharField(max_length=20,verbose_name='客队进球')
    time = models.DateTimeField(verbose_name='比赛日期')    
 
    class Meta:
        ordering = ['-time']    

# class VisitingTeams(models.Model):
#     country = models.CharField(max_length=30,verbose_name='球队')
#     group_id = models.CharField(max_length=10,verbose_name='小组')
#     score = models.OneToOneField(Score)


