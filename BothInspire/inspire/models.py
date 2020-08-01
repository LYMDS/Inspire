from django.db import models

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    fullname = models.CharField(max_length=10)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    sex = models.BooleanField()
    sweet = models.IntegerField()
    head_img = models.FileField(default="files/head_img.jpg", upload_to="files/")
    cp_group = models.CharField(max_length=36, default="fd8f6ce0-c2bb-4dbe-bc72-16a843d1ea7a")

class Mission(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    reason = models.TextField()
    sweet = models.IntegerField()
    # 审核状态
    approval_status = models.IntegerField()
    # 申请人
    applicant = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_applicant')
    # 审核人
    reviewer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_reviewer')
    # 文件组
    file_group = models.CharField(max_length=36, null=True)
    created = models.DateTimeField()

class File(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    group = models.CharField(max_length=36)
    file = models.FileField(default="files/default.jpg", upload_to="files/")

class Gift(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    img = models.FileField(default="files/gift.jpg", upload_to="files/")
    title = models.CharField(max_length=50)
    sweet = models.IntegerField()
    createdby = models.ForeignKey('User', on_delete=models.CASCADE)
    count = models.IntegerField()
    isexchange = models.BooleanField()
    created = models.DateTimeField()

class LoginSession(models.Model):
    sessionid = models.CharField(max_length=36, primary_key=True)
    sessiondata = models.TextField()
    expire_time = models.DateTimeField()


