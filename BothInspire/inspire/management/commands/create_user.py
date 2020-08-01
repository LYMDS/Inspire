from django.core.management import BaseCommand
from django.contrib.sessions.backends.db import SessionStore
import hashlib
import uuid as IDGetter
from inspire.models import User
class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **options):
        if User.objects.all().count() >= 2:
            print("不能再注册用户啦！")
            return
        id = IDGetter.uuid4().__str__()
        name = input("名字：")
        username = input("用户名：")
        password = input("密码：")
        password = hashlib.md5(password.encode()).hexdigest().upper()
        sex = input("性别：")
        while sex != "男" and sex != "女":
            print("输入性别有误")
            sex = input("性别：")
        if sex == "男":
            sex = True
        else:
            sex = False
        user = User()
        user.id = id
        user.fullname = name
        user.username = username
        user.password = password
        user.sex = sex
        user.sweet = 0
        user.save()
        print("success")