from django.db import models
from alpine_gp.models import Course

# Create your models here.


class Admission(models.Model):
    student_id = models.AutoField(primary_key=True, editable=True, null=False)
    college_id = models.IntegerField(editable=True, null=False, blank=False)
    crsid = models.CharField(editable=True, null=False, blank=False)
    ssnid = models.IntegerField(editable=True, null=False, blank=False)
    enrol_id = models.CharField(
        editable=True, null=False, blank=False, max_length=100, unique=True
    )
    stu_name = models.CharField(max_length=200)
    doj = models.CharField(max_length=200)
    contact_no = models.BigIntegerField(editable=True)

    admsn_yr1 = models.IntegerField(editable=True, null=True, blank=True)
    admsn_yr2 = models.IntegerField(editable=True, null=True, blank=True)
    admsn_yr3 = models.IntegerField(editable=True, null=True, blank=True)
    admsn_yr4 = models.IntegerField(editable=True, null=True, blank=True)
    admsn_yr5 = models.IntegerField(editable=True, null=True, blank=True)
    admsn_yr6 = models.IntegerField(editable=True, null=True, blank=True)

    security_fee = models.IntegerField(editable=True, null=True, blank=True)
    other_fee = models.IntegerField(editable=True, null=True, blank=True)
    yr1_fee = models.IntegerField(editable=True, null=True, blank=True)
    yr2_fee = models.IntegerField(editable=True, null=True, blank=True)
    yr3_fee = models.IntegerField(editable=True, null=True, blank=True)
    yr4_fee = models.IntegerField(editable=True, null=True, blank=True)
    yr5_fee = models.IntegerField(editable=True, null=True, blank=True)
    yr6_fee = models.IntegerField(editable=True, null=True, blank=True)
    ref_by = models.IntegerField(null=True, blank=True)
    is_paid = models.CharField(max_length=20, null=True, blank=True)
    remark = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.stu_name)


class Profile(models.Model):
    student = models.OneToOneField(Admission, on_delete=models.CASCADE)
    mother_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    category = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100)
    permanent_address = models.TextField()
    correspondence_address = models.TextField(null=True)
    state = models.CharField(max_length=100)
    id_type = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50)
    parent_phone = models.CharField(max_length=20, null=True)
    guardian_phone = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True)
    exam_passed = models.CharField(max_length=100)
    year_of_passing = models.PositiveIntegerField()
    university_board = models.CharField(max_length=100)
    marks_percentage = models.CharField(max_length=100)
    card_1 = models.CharField(max_length=50, null=True)
    card_2 = models.CharField(max_length=50, null=True)
    card_3 = models.CharField(max_length=50, null=True)
    card_4 = models.CharField(max_length=50, null=True)
    eno_1 = models.CharField(max_length=50, null=True)
    eno_2 = models.CharField(max_length=50, null=True)
    eno_3 = models.CharField(max_length=50, null=True)
    eno_4 = models.CharField(max_length=50, null=True)
    eno_5 = models.CharField(max_length=50, null=True)
    eno_6 = models.CharField(max_length=50, null=True)
    eno_7 = models.CharField(max_length=50, null=True)
    eno_8 = models.CharField(max_length=50, null=True)

    def __str__(self) -> str:
        return str(self.student)


PROMOTION_STATUS_CHOICES = [
    ("new_admission", "New Admission"),
    ("promoted", "Promoted"),
    ("not_promoted", "Not Promoted"),
    ("passed", "Passed"),
    ("suspended", "Suspended"),
]


class Promotion(models.Model):
    student = models.OneToOneField(Admission, on_delete=models.CASCADE)
    curr_year = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=PROMOTION_STATUS_CHOICES, default="not_passed"
    )
    _duration = models.IntegerField(editable=False, blank=True, null=True)

    @property
    def duration(self):
        if self._duration is None:
            self._duration = Course.objects.get(crsid=self.student.crsid).duration
        return self._duration

    def save(self, *args, **kwargs):
        self._duration = self.duration  # Update _duration before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self._duration}"
