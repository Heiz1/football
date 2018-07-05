from django.shortcuts import render
from .models import *
from django.http import request, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 返回导航页
def index(request):
    return render(request, 'index.html')


# 积分榜
def score(request):
    # 获取url的页面参数(GET请求)
    page_num = request.GET.get('page', 1)

    # 查询结果集
    teams_all_list = Scores.objects.all()
    # 每页多少条记录
    # 每页信息数量
    per_page = 8
    # 每8条信息进行分页
    paginator = Paginator(teams_all_list, per_page)
    try:
        context = paginator.page(page_num)
    # 无效的转至第一页
    except PageNotAnInteger:
        context = paginator.page(1)
    except EmptyPage:
        context = paginator.page(paginator.num_pages)
    # 获取当前页码,即第几页
    page = context.number
    # 页码优化,如果当页码数多时,中间用'...'隐藏
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(page - 2, 1), page)) + \
        list(range(page, min(page + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    return render(request, 'all.html', {'context': context, 'page_range': page_range})


# 每小组净胜球最多
def mostgoal_difference(request):
    # 获取分组结果集
    GroupInfos = Groups.objects.all().values('id')
    # 分组情况
    groups = []
    for GroupInfo in GroupInfos:
        group = GroupInfo['id']
        if group not in groups:
            groups.append(group)
    # 净胜球最多的队伍
    mostgoal_difference_teams = {}
    # 每组的国家
    for group_id in groups:
        teaminfos = Scores.objects.filter(group_id=group_id)
        group = Groups.objects.get(id=group_id).group
        # 当前组每队的净胜球
        goal_differences= []
        for teaminfo in teaminfos:
            goal_differences.append(teaminfo.goal_difference)
        mostgoal_differences=max(goal_differences)
        mostgoal_difference=max(mostgoal_differences)
        
        mostgoal_difference_team_info= Scores.objects.filter(group_id=group_id,
                                    goal_difference=mostgoal_difference)[0]
        
        mostgoal_difference_team_id = mostgoal_difference_team_info.team_id
        mostgoal_difference_team = Teams.objects.filter(id=mostgoal_difference_team_id)[0]
        # 把当前组作为键，净胜球最多的队伍作为值
        mostgoal_difference_teams[group] = mostgoal_difference_team.team
    

    return render(request, 'mostgoal.html',locals())


# 返回比分差距最大的3场比赛记录(按照比赛日期逆序排序)
def score_difference(request):
    # info = GameInfo.objects.raw('select * from index_gameinfo')
    info = GameInfo.objects.raw(
        'select * from (select *, abs(HomeTeam_score-VisitingTeams_score) as score_difference from (select * from index_gameinfo order by time DESC) order by score_difference DESC limit 0,3) order by time DESC')
    return render(request,'score_difference.html',locals())


# 返回每个小组晋级的两只球队(排名优先级：积分、净胜球、球队名)
def promotion(request):
            
    # 获取分组结果集
    GroupInfos = Groups.objects.all().values('id')
    # 分组情况
    groups = []
    for GroupInfo in GroupInfos:
        group = GroupInfo['id']
        if group not in groups:
            groups.append(group)
    
    teams={}
    for group_id in groups:
        group = Groups.objects.get(id=group_id).group
        teaminfo_first = Scores.objects.filter(group_id=group_id)[0]
        teaminfo_second = Scores.objects.filter(group_id=group_id)[1]
        teams[group+'组第1名'] = teaminfo_first
        teams[group+'组第2名'] = teaminfo_second           

    return render(request,'promotion.html',locals()) 




# 添加队伍积分榜信息
def add(request):

    # 主队
    HomeTeamsInfo = GameInfo.objects.all().values(
        'HomeTeam', 'groups','HomeTeam_score', 'VisitingTeams_score')

    for HomeTeamInfo in HomeTeamsInfo:
        group = HomeTeamInfo['groups']
        HomeTeam = HomeTeamInfo['HomeTeam']
        HomeTeam_score = HomeTeamInfo['HomeTeam_score']
        VisitingTeams_score = HomeTeamInfo['VisitingTeams_score']
        if int(HomeTeam_score) > int(VisitingTeams_score):
            score = 3
        elif int(HomeTeam_score) == int(VisitingTeams_score):
            score = 1
        else:
            score = 0
        goal_difference = int(HomeTeam_score) - int(VisitingTeams_score)
        teaminfo = Scores.objects.filter(team_id=HomeTeam)
        # 判断队伍在数据库中是否存在
        if teaminfo:
            teaminfo = Scores.objects.get(team_id=HomeTeam)
            teaminfo.goal = int(teaminfo.goal)+int(HomeTeam_score)
            teaminfo.lost = int(teaminfo.lost)+int(VisitingTeams_score)
            teaminfo.goal_difference = int(teaminfo.goal_difference) +\
                int(goal_difference)
            teaminfo.score = int(teaminfo.score)+int(score)
        # 队伍不存在则在数据库创建
        else:
            teaminfo = Scores(team_id=HomeTeam, group_id=group,
                              goal=HomeTeam_score, lost=VisitingTeams_score,
                              goal_difference=goal_difference, score=score)
        teaminfo.save()

    # 客队
    VisitingTeamsInfo = GameInfo.objects.all().values(
        'VisitingTeams','HomeTeam_score', 'VisitingTeams_score')

    for VisitingTeamInfo in VisitingTeamsInfo:
        VisitingTeam = VisitingTeamInfo['VisitingTeams']
        HomeTeam_score = VisitingTeamInfo['HomeTeam_score']
        VisitingTeam_score = VisitingTeamInfo['VisitingTeams_score']
        if int(VisitingTeam_score) > int(HomeTeam_score):
            score = 3
        elif int(HomeTeam_score) == int(VisitingTeam_score):
            score = 1
        else:
            score = 0
        goal_difference = int(VisitingTeam_score) - int(HomeTeam_score)

        teaminfo = Scores.objects.get(team_id=VisitingTeam)
        teaminfo.goal = int(teaminfo.goal)+int(VisitingTeam_score)

        teaminfo.lost = int(teaminfo.lost)+int(HomeTeam_score)
        teaminfo.goal_difference = int(teaminfo.goal_difference) +\
            int(goal_difference)
        teaminfo.score = int(teaminfo.score)+int(score)

        teaminfo.save()
    return HttpResponse('添加成功')


# 删除数据
def delete_data(request):
    data = Scores.objects.all()
    data.delete()
    return render(request,'index.html')