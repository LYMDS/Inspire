from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from .models import *
import datetime
#
from .Tools.GuidHelper import *
# 过期检测
from .Tools.DateTimeHelper import expire_checker
# 自定义Session助手
from .Tools.SessionHelper import *
import hashlib
import json
from .Tools.DropListHelpr import ApprovalStatus

#@method_decorator(ensure_csrf_cookie)
def upfile(request):
    print(request.method)
    if request.method == 'POST':
        missionId = request.POST.get("missionId")
        fileGroup = request.POST.get("fileGroupId")
        limit = True
        try:
            # 查看是否在之前就有任务单
            mission = Mission.objects.get(id=missionId)
            # Mission表里的的文件组
            formFileGroup = mission.file_group
            # 如果文件组是正常的
            if formFileGroup is not None and len(formFileGroup) == 36:
                # Mission原有的文件组
                fileGroup = formFileGroup
                # 查询原有的文件组的文件数量
                fileGroupCount = File.objects.filter(group=fileGroup).count()
                # 文件组数量不能超过9个
                if fileGroupCount >= 9:
                    limit = False
            else:
                return JsonResponse({'msg': 'have not fileGroupid'})
        except Mission.DoesNotExist:
            # 没有该任务单
            return JsonResponse({'msg': 'have not mission'})

        if limit:
            # 创建文件
            file = File()
            file.id = Guid()
            file.group = fileGroup
            file.file = request.FILES.get("file")
            file.save()
            return JsonResponse({'msg': 'success'})
        else:
            return JsonResponse({'msg': 'out of limit 9'})
    return JsonResponse({'msg': 'request method isn\'t POST'})

def create_mission(request):
    payload = json.loads(request.body.decode())
    # 获取参数
    missionid = payload["missionid"]
    context = payload["context"]
    sweet = payload["sweet"]
    sessionid = payload["sessionid"]
    sessionData = GetSessionData(sessionid)
    if IsGuid(missionid):
        # 更新
        mission = Mission.objects.get(id=missionid)
        mission.reason = context
        mission.sweet = sweet
        mission.save()
        return JsonResponse({
            'missionId': mission.id,
            'fileGroupId': mission.file_group
        })
    else:
        # 创建
        mission = Mission()
        formid = Guid()
        filegroupid = Guid()
        mission.id = formid
        mission.sweet = sweet
        mission.reason = context
        mission.approval_status = 0
        mission.applicant = User.objects.get(id=sessionData["userid"])
        mission.reviewer = User.objects.get(~Q(id=sessionData["userid"]), cp_group='fd8f6ce0-c2bb-4dbe-bc72-16a843d1ea7a')
        mission.file_group = filegroupid
        mission.created = datetime.datetime.now()
        mission.save()
        return JsonResponse({
            'missionId': formid,
            'fileGroupId': filegroupid
        })

def check_login_status(request):
    payload = json.loads(request.body.decode())
    # 获取sessionid
    sessionid = payload["sessionid"]
    if sessionid == None or len(sessionid) != 36:
        return JsonResponse({"state": False})
    else:
        try:
            sessionData = GetSessionData(sessionid)
            userid = sessionData["userid"]
            if userid != '' and len(userid) == 36 and expire_checker(sessionData["expire_time"]):
                fullname = User.objects.get(id=userid).fullname
                return JsonResponse({"state": True, "fullname": fullname})
            else:
                return JsonResponse({"state": False})
        except LoginSession.DoesNotExist:
            return JsonResponse({"state": False})

def login(request):
    payload = json.loads(request.body.decode())
    username = payload["username"]
    password = payload["password"]
    respose_data = {'msg': 'no option'}
    try:
        user = User.objects.get(username=username)
        password = hashlib.md5(password.encode()).hexdigest().upper()
        if password == user.password:
            sessionid = CreateNewSession(user.id)
            respose_data['fullname'] = user.fullname
            respose_data['sessionid'] = sessionid
            respose_data['msg'] = 'success'
        else:
            respose_data['msg'] = 'PasswordFailed'
    except User.DoesNotExist:
        respose_data['msg'] = 'NotExistThisUser'
    return JsonResponse(respose_data)

def sendbymyself(request):
    payload = json.loads(request.body.decode())
    sessionid = payload["sessionid"]
    user = GetUserSessionData(sessionid)
    if user == None:
        return JsonResponse({
            "msg": "NotExistThisUser"
        })
    data = []
    missions = Mission.objects.filter(applicant=user)
    approvalStatus = ApprovalStatus()
    for i in missions:
        mission = {
            'id': i.id,
            'reason': i.reason,
            'sweet': i.sweet,
            'approval_status': approvalStatus.getOption(i.approval_status),
            'applicant': i.applicant.fullname,
            'reviewer': i.reviewer.fullname,
            'file_group': i.file_group,
            'created': i.created.strftime('%Y-%m-%d %H:%M')
        }
        data.append(mission)
    return JsonResponse({
        "msg": "success",
        "missions": data
    })

def approved(request):
    payload = json.loads(request.body.decode())
    sessionid = payload["sessionid"]
    user = GetUserSessionData(sessionid)
    if user == None:
        return JsonResponse({
            "msg": "NotExistThisUser"
        })
    data = []
    missions = Mission.objects.filter(Q(applicant=user)|Q(reviewer=user), approval_status=2)
    approvalStatus = ApprovalStatus()
    for i in missions:
        mission = {
            'id': i.id,
            'reason': i.reason,
            'sweet': i.sweet,
            'approval_status': approvalStatus.getOption(i.approval_status),
            'applicant': i.applicant.fullname,
            'reviewer': i.reviewer.fullname,
            'file_group': i.file_group,
            'created': i.created.strftime('%Y-%m-%d %H:%M')
        }
        data.append(mission)
    return JsonResponse({
        "msg": "success",
        "missions": data
    })

def approving(request):
    payload = json.loads(request.body.decode())
    sessionid = payload["sessionid"]
    user = GetUserSessionData(sessionid)
    if user == None:
        return JsonResponse({
            "msg": "NotExistThisUser"
        })
    data = []
    missions = Mission.objects.filter(Q(applicant=user)|Q(reviewer=user), approval_status=1)
    approvalStatus = ApprovalStatus()
    for i in missions:
        mission = {
            'id': i.id,
            'reason': i.reason,
            'sweet': i.sweet,
            'approval_status': approvalStatus.getOption(i.approval_status),
            'applicant': i.applicant.fullname,
            'reviewer': i.reviewer.fullname,
            'file_group': i.file_group,
            'created': i.created.strftime('%Y-%m-%d %H:%M')
        }
        data.append(mission)
    return JsonResponse({
        "msg": "success",
        "missions": data
    })

def getfilesurl(request):
    fileGroup = request.GET.get("fileGroup")
    files = File.objects.filter(group=fileGroup)
    fileList = []
    for i in files:
        data = {
            "id": i.id,
            "filename": i.file.name,
            "url": request.META['wsgi.url_scheme'] + "://" + request.META['HTTP_HOST'] + "/media/" + i.file.name
        }
        fileList.append(data)
    return JsonResponse({"files": fileList})

def save_mission(request):
    payload = json.loads(request.body.decode())
    missionid = payload["id"]
    reason = payload["reason"]
    sweet = payload["sweet"]
    try:
        mission = Mission.objects.get(id=missionid)
        mission.reason = reason
        mission.sweet = sweet
        mission.save()
        return JsonResponse({"msg": "success"})
    except Mission.DoesNotExist:
        return JsonResponse({"msg": "not find mission"})

def delete_file(request):
    payload = json.loads(request.body.decode())
    fileid = payload["id"]
    file = File.objects.get(id=fileid)
    # 删除文件
    file.file.delete()
    # 删除数据
    file.delete()
    return JsonResponse({"msg": "success"})

# 获取当前用户的审核权限
def getapprovalprivilege(request):
    sessionid = request.GET.get("sessionid")
    missionid = request.GET.get("missionid")
    userid = GetUserSessionData(sessionid).id
    mission_userid = Mission.objects.get(id=missionid).reviewer_id
    if userid == mission_userid:
        return JsonResponse({"approvalPrivilege": True})
    else:
        return JsonResponse({"approvalPrivilege": False})

def change_mission_status(request):
    payload = json.loads(request.body.decode())
    missionid = payload["missionid"]
    status = int(payload["status"])
    mission = Mission.objects.get(id=missionid)
    mission.approval_status = status
    mission.save()
    if status == 2:
        mission.applicant.sweet += mission.sweet
    elif status == 5:
        mission.applicant.sweet -= (mission.sweet // 2)
    mission.applicant.save()
    return JsonResponse({"msg": "success"})

def getMissionById(request):
    missionid = request.GET.get("missionid")
    mission = Mission.objects.get(id=missionid)
    approvalStatus = ApprovalStatus()
    data = {
        'id': mission.id,
        'reason': mission.reason,
        'sweet': mission.sweet,
        'approval_status': approvalStatus.getOption(mission.approval_status),
        'applicant': mission.applicant.fullname,
        'reviewer': mission.reviewer.fullname,
        'file_group': mission.file_group,
        'created': mission.created.strftime('%Y-%m-%d %H:%M')
    }
    return JsonResponse({
        "msg": "success",
        "missiondata": data
    })

def changeHeadImg(request):
    sessionid = request.POST.get("sessionid")
    user = GetUserSessionData(sessionid)
    user.head_img = request.FILES.get("file")
    user.save()
    return JsonResponse({"msg": "success"})

def getMetaInfo(request):
    sessionid = request.GET.get("sessionid")
    user = GetUserSessionData(sessionid)
    url = request.META['wsgi.url_scheme'] + "://" + request.META['HTTP_HOST'] + "/media/" + user.head_img.file.name
    return JsonResponse({"msg": "success", "url": url, "sweet": user.sweet})

def publicGift(request):
    id = request.POST.get("id")
    sessionid = request.POST.get("sessionid")
    user = GetUserSessionData(sessionid)
    file = request.FILES.get("file")
    sweet = request.POST.get("sweet")
    count = request.POST.get("count")
    title = request.POST.get("title")
    # 新建
    if id is None or not IsGuid(id):
        gift = Gift()
        gift.id = Guid()
        gift.img = file
        gift.title = title
        gift.sweet = sweet
        gift.createdby = user
        gift.count = count
        gift.isexchange = True
        gift.created = datetime.datetime.now()
        gift.save()
        return JsonResponse({"id": gift.id})
    # 修改
    else:
        gift = Gift.objects.get(id=id)
        gift.img = file
        gift.title = title
        gift.sweet = sweet
        gift.count = count
        gift.save()
        return JsonResponse({"id": gift.id})





