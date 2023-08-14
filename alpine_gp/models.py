from django.db import models

# Create your models here.


class College(models.Model):
    college_id = models.AutoField(primary_key=True, editable=False, null=False)
    college_code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=200)
    affiliation = models.CharField(max_length=200, null=True)
    approved_by = models.CharField(max_length=200, null=True)
    status = models.IntegerField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return str(self.name)


class Course(models.Model):
    crsid = models.CharField(max_length=20, primary_key=True, editable=False, unique=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True)
    course = models.CharField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return str(self.course)


class Session(models.Model):
    ssnid = models.AutoField(primary_key=True, editable=False)

    ssntitle = models.TextField(null=False, blank=False)
    sdate = models.CharField(null=False, blank=False)
    edate = models.CharField(null=False, blank=False)
    iscurrent = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return str(self.ssntitle)


class Agent(models.Model):
    agentsid = models.BigIntegerField(primary_key=True)
    agentname = models.CharField(null=True, blank=True)
    email = models.EmailField(null=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return str(self.agentname)
