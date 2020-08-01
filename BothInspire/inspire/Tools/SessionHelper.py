from ..models import LoginSession
from ..models import User
from .GuidHelper import Guid
import json
import datetime as dt
def CreateNewSession(userid):
    newGuid = Guid()
    newSession = LoginSession()
    newSession.sessionid = newGuid
    newSession.sessiondata = '{"userid": "%s"}'%userid
    newSession.expire_time = dt.datetime.now() + dt.timedelta(days=1)
    newSession.save()
    return newGuid

def GetSessionData(sessionid):
    try:
        session = LoginSession.objects.get(sessionid=sessionid)
        return {
            "userid": json.loads(session.sessiondata)["userid"],
            "expire_time": session.expire_time
        }
    except LoginSession.DoesNotExist:
        return None

def GetUserSessionData(sessionid):
    try:
        session = LoginSession.objects.get(sessionid=sessionid)
        userid = json.loads(session.sessiondata)["userid"]
        try:
            return User.objects.get(id=userid)
        except:
            return None
    except LoginSession.DoesNotExist:
        return None

def GetCpGroupFromSessionData(sessionid):
    # 获取当前用户
    user = GetUserSessionData(sessionid)
    if user != None:
        # 取当前用户的用户组作为条件筛选一对情侣
        cpGroup = User.objects.filter(cp_group=user.cp_group)
        cpData = {}
        # 要求返回的条数为2
        if cpGroup.count() == 2:
            for i in cpGroup:
                # 判断男生 女生
                if i.sex:
                    cpData["boy"] = i
                else:
                    cpData["girl"] = i
        else:
            return None
    else:
        return None